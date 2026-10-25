"""Explicit local emulator for the LangMem-shaped prototype interface."""

from __future__ import annotations

from typing import Any

import numpy as np

from sentinelmem.backends.base import BaseMemoryBackend, EmbeddingFn, SearchResult
from sentinelmem.models import MemoryRecord


class EmulatedLangMemBackend(BaseMemoryBackend):
    """In-memory interface emulator; it does not import LangGraph or LangMem."""

    def __init__(self, embedding_dimension: int | None = None, embedding_fn: EmbeddingFn | None = None, *, embedder: Any | None = None, audit_ledger: Any | None = None) -> None:
        super().__init__(embedding_dimension, embedding_fn, embedder=embedder, audit_ledger=audit_ledger)
        self._records: dict[str, MemoryRecord] = {}

    @property
    def name(self) -> str:
        return "emulated_langmem"

    def _write_records(self, records: list[MemoryRecord]) -> list[str]:
        for record in records:
            self._records[record.record_id] = record
        return [record.record_id for record in records]

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        if top_k <= 0 or not self._records:
            return []
        records = list(self._records.values())
        matrix = np.vstack([self.embedding_fn(record.text, self.embedding_dimension) for record in records])
        query_vector = self.embedding_fn(query, self.embedding_dimension)
        scores = matrix @ query_vector
        ranked = np.argsort(scores)[::-1][:top_k]
        return [SearchResult(records[i].record_id, records[i].text, records[i].label, records[i].provenance, round(float(scores[i]), 8), {"backend": self.name, "thread_id": "default", **records[i].metadata}) for i in ranked]

    def delete(self, record_id: str) -> bool:
        return self._records.pop(record_id, None) is not None

    def list(self) -> list[MemoryRecord]:
        return list(self._records.values())

    def count(self) -> int:
        return len(self._records)

    def clear(self) -> None:
        self._records.clear()
