"""LangMem memory backend adapter for SentinelMem."""

from __future__ import annotations

from typing import Any, Callable
import numpy as np

from sentinelmem.backends.base import BaseMemoryBackend, EmbeddingFn, SearchResult
from sentinelmem.synthetic import MemoryRecord


class LangMemBackend(BaseMemoryBackend):
    """Memory backend adapter for LangGraph / LangChain LangMem memory manager."""

    def __init__(
        self,
        embedding_dimension: int = 64,
        embedding_fn: EmbeddingFn | None = None,
    ) -> None:
        super().__init__(embedding_dimension=embedding_dimension, embedding_fn=embedding_fn)
        self._threads: dict[str, list[MemoryRecord]] = {"default": []}
        self._vector_matrix: list[np.ndarray] = []
        self._all_records: list[MemoryRecord] = []

    @property
    def name(self) -> str:
        return "langmem"

    def add(self, records: list[MemoryRecord]) -> list[str]:
        added_ids: list[str] = []
        for record in records:
            vec = self.embedding_fn(record.text, self.embedding_dimension)
            self._threads["default"].append(record)
            self._all_records.append(record)
            self._vector_matrix.append(vec)
            added_ids.append(record.record_id)
        return added_ids

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        if not self._all_records or top_k <= 0:
            return []

        query_vec = self.embedding_fn(query, self.embedding_dimension)
        matrix = np.vstack(self._vector_matrix)
        scores = np.dot(matrix, query_vec)
        ranked_indices = np.argsort(scores)[::-1][: min(top_k, len(self._all_records))]

        results: list[SearchResult] = []
        for idx in ranked_indices:
            record = self._all_records[idx]
            results.append(
                SearchResult(
                    record_id=record.record_id,
                    text=record.text,
                    label=record.label,
                    provenance=record.provenance,
                    score=round(float(scores[idx]), 8),
                    metadata={"backend": "langmem", "thread_id": "default", **record.metadata}
                )
            )
        return results

    def count(self) -> int:
        return len(self._all_records)

    def clear(self) -> None:
        self._threads = {"default": []}
        self._all_records.clear()
        self._vector_matrix.clear()
