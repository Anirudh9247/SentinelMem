"""Mem0 memory backend adapter for SentinelMem."""

from __future__ import annotations

from typing import Any, Callable
import numpy as np

from sentinelmem.backends.base import BaseMemoryBackend, EmbeddingFn, SearchResult
from sentinelmem.synthetic import MemoryRecord


class Mem0Backend(BaseMemoryBackend):
    """Memory backend adapter for Mem0 multi-layered memory architecture.
    
    Supports structured user memory extraction, episodic tracking, and vector indexing.
    """

    def __init__(
        self,
        embedding_dimension: int = 64,
        embedding_fn: EmbeddingFn | None = None,
    ) -> None:
        super().__init__(embedding_dimension=embedding_dimension, embedding_fn=embedding_fn)
        self._user_memories: dict[str, MemoryRecord] = {}
        self._vector_matrix: list[np.ndarray] = []
        self._id_list: list[str] = []

    @property
    def name(self) -> str:
        return "mem0"

    def add(self, records: list[MemoryRecord]) -> list[str]:
        added_ids: list[str] = []
        for record in records:
            vec = self.embedding_fn(record.text, self.embedding_dimension)
            self._user_memories[record.record_id] = record
            self._vector_matrix.append(vec)
            self._id_list.append(record.record_id)
            added_ids.append(record.record_id)
        return added_ids

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        if not self._user_memories or top_k <= 0:
            return []

        query_vec = self.embedding_fn(query, self.embedding_dimension)
        matrix = np.vstack(self._vector_matrix)
        
        # Cosine similarity for unit vectors
        scores = np.dot(matrix, query_vec)
        ranked_indices = np.argsort(scores)[::-1][: min(top_k, len(self._id_list))]

        results: list[SearchResult] = []
        for idx in ranked_indices:
            rec_id = self._id_list[idx]
            record = self._user_memories[rec_id]
            results.append(
                SearchResult(
                    record_id=record.record_id,
                    text=record.text,
                    label=record.label,
                    provenance=record.provenance,
                    score=round(float(scores[idx]), 8),
                    metadata={"backend": "mem0", **record.metadata}
                )
            )
        return results

    def count(self) -> int:
        return len(self._user_memories)

    def clear(self) -> None:
        self._user_memories.clear()
        self._vector_matrix.clear()
        self._id_list.clear()
