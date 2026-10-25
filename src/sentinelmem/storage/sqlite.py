"""SQLite persistence for write provenance, security events, and quarantine."""

from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

from sentinelmem.models import MemoryRecord


def _canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


class SQLiteLedger:
    """Small local ledger whose data survives closing and reopening the process."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=30)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self) -> None:
        with self._connect() as connection:
            connection.executescript(
                """
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS provenance (
                    record_id TEXT PRIMARY KEY,
                    source TEXT NOT NULL,
                    session_id TEXT NOT NULL,
                    agent_id TEXT NOT NULL,
                    written_at REAL NOT NULL,
                    content_hash TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS quarantine (
                    record_id TEXT PRIMARY KEY,
                    record_json TEXT NOT NULL,
                    reason TEXT NOT NULL,
                    trust_score REAL,
                    created_at REAL NOT NULL,
                    status TEXT NOT NULL DEFAULT 'quarantined'
                );
                CREATE TABLE IF NOT EXISTS audit_events (
                    sequence INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    previous_hash TEXT NOT NULL,
                    event_hash TEXT NOT NULL UNIQUE
                );
                CREATE TRIGGER IF NOT EXISTS audit_events_no_update
                BEFORE UPDATE ON audit_events BEGIN
                    SELECT RAISE(ABORT, 'audit events are append-only');
                END;
                CREATE TRIGGER IF NOT EXISTS audit_events_no_delete
                BEFORE DELETE ON audit_events BEGIN
                    SELECT RAISE(ABORT, 'audit events are append-only');
                END;
                """
            )

    def _append_event(self, connection: sqlite3.Connection, event_type: str, payload: dict[str, Any]) -> None:
        previous = connection.execute(
            "SELECT event_hash FROM audit_events ORDER BY sequence DESC LIMIT 1"
        ).fetchone()
        previous_hash = previous["event_hash"] if previous else "0" * 64
        timestamp = time.time()
        payload_json = _canonical(payload)
        canonical_event = _canonical({
            "event_type": event_type,
            "payload": payload,
            "previous_hash": previous_hash,
            "timestamp": timestamp,
        })
        event_hash = hashlib.sha256(canonical_event.encode("utf-8")).hexdigest()
        connection.execute(
            "INSERT INTO audit_events(event_type,payload_json,timestamp,previous_hash,event_hash) VALUES(?,?,?,?,?)",
            (event_type, payload_json, timestamp, previous_hash, event_hash),
        )

    def record_write(self, record: MemoryRecord) -> None:
        """Persist provenance and a matching audit entry for every backend write."""
        if record.written_at is None or record.content_hash is None or record.source is None:
            raise ValueError("record must be stamped with write-time provenance before persistence")
        payload = {
            "record_id": record.record_id,
            "source": record.source,
            "session_id": record.session_id or "default",
            "agent_id": record.agent_id or "sentinelmem",
            "written_at": record.written_at,
            "content_hash": record.content_hash,
        }
        with self._connect() as connection:
            connection.execute(
                "INSERT OR REPLACE INTO provenance(record_id,source,session_id,agent_id,written_at,content_hash) VALUES(?,?,?,?,?,?)",
                (record.record_id, payload["source"], payload["session_id"], payload["agent_id"], record.written_at, record.content_hash),
            )
            self._append_event(connection, "memory_written", payload)

    def quarantine_record(self, record: MemoryRecord, reason: str, trust_score: float | None = None) -> None:
        """Persist a local synthetic or research record pending review."""
        created_at = time.time()
        payload = asdict(record)
        with self._connect() as connection:
            connection.execute(
                "INSERT OR REPLACE INTO quarantine(record_id,record_json,reason,trust_score,created_at,status) VALUES(?,?,?,?,?,'quarantined')",
                (record.record_id, _canonical(payload), reason, trust_score, created_at),
            )
            self._append_event(connection, "record_quarantined", {
                "record_id": record.record_id,
                "reason": reason,
                "trust_score": trust_score,
                "created_at": created_at,
            })

    def get_provenance(self, record_id: str) -> dict[str, Any] | None:
        with self._connect() as connection:
            row = connection.execute("SELECT * FROM provenance WHERE record_id=?", (record_id,)).fetchone()
        return dict(row) if row else None

    def list_quarantine(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute("SELECT * FROM quarantine ORDER BY created_at, record_id").fetchall()
        items = []
        for row in rows:
            item = dict(row)
            item["record"] = json.loads(item.pop("record_json"))
            items.append(item)
        return items

    def list_audit_events(self) -> list[dict[str, Any]]:
        with self._connect() as connection:
            rows = connection.execute("SELECT * FROM audit_events ORDER BY sequence").fetchall()
        return [dict(row) for row in rows]

    def verify_audit_chain(self) -> bool:
        expected_previous = "0" * 64
        for row in self.list_audit_events():
            payload = json.loads(row["payload_json"])
            if row["previous_hash"] != expected_previous:
                return False
            canonical_event = _canonical({
                "event_type": row["event_type"],
                "payload": payload,
                "previous_hash": expected_previous,
                "timestamp": row["timestamp"],
            })
            actual_hash = hashlib.sha256(canonical_event.encode("utf-8")).hexdigest()
            if actual_hash != row["event_hash"]:
                return False
            expected_previous = actual_hash
        return True
