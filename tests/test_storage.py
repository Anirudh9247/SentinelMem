"""SQLite provenance and persistence tests."""

from sentinelmem.backends import FAISSBackend
from sentinelmem.models import MemoryRecord
from sentinelmem.storage import SQLiteLedger


def test_write_provenance_and_audit_survive_reopen(tmp_path):
    database = tmp_path / "research.sqlite3"
    ledger = SQLiteLedger(database)
    backend = FAISSBackend(embedding_dimension=64, audit_ledger=ledger)
    record = MemoryRecord("m-restart", "Synthetic local record", provenance="untrusted_import")
    backend.write(record, session_id="session-7", agent_id="agent-a")

    reopened = SQLiteLedger(database)
    provenance = reopened.get_provenance("m-restart")
    assert provenance is not None
    assert provenance["source"] == "untrusted_import"
    assert provenance["session_id"] == "session-7"
    assert provenance["agent_id"] == "agent-a"
    assert len(provenance["content_hash"]) == 64
    assert len(reopened.list_audit_events()) == 1
    assert reopened.verify_audit_chain()


def test_quarantine_survives_reopen(tmp_path):
    database = tmp_path / "quarantine.sqlite3"
    record = MemoryRecord("m-quarantine", "Synthetic suspicious placeholder", label="instruction_shaped")
    SQLiteLedger(database).quarantine_record(record, "fixture review", 0.25)

    reopened_items = SQLiteLedger(database).list_quarantine()
    assert len(reopened_items) == 1
    assert reopened_items[0]["record"]["record_id"] == record.record_id
    assert reopened_items[0]["reason"] == "fixture review"
    assert reopened_items[0]["status"] == "quarantined"
    assert SQLiteLedger(database).verify_audit_chain()
