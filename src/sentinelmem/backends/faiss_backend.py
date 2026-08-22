"""FAISS vector database memory backend adapter."""

from __future__ import annotations

from typing import Any, Callable
import numpy as np

from sentinelmem.backends.base import BaseMemoryBackend, EmbeddingFn, SearchResult
from sentinelmem.synthetic import MemoryRecord


class FAISSBackend(BaseMemoryBackend):
    """Memory backend adapter powered by FAISS (IndexFlatIP)."""

    def __init__(
        self,
        embedding_dimension: int = 64,
        embedding_fn: EmbeddingFn | None = None,
        index_type: str = "FlatIP",
    ) -> None:
        super().__init__(embedding_dimension=embedding_dimension, embedding_fn=embedding_fn)
        self.index_type = index_type
        self._records: list[MemoryRecord] = []
        self._index: Any = None
        self._init_index()

    def _init_index(self) -> None:
        try:
            import faiss
        except ImportError as error:
            raise RuntimeError(
                "faiss-cpu is required to use FAISSBackend; install project dependencies."
            ) from error

        if self.index_type == "FlatIP":
            self._index = faiss.IndexFlatIP(self.embedding_dimension)
        elif self.index_type == "FlatL2":
            self._index = faiss.IndexFlatL2(self.embedding_dimension)
        else:
            raise ValueError(f"Unsupported FAISS index_type: {self.index_type}")

    @property
    def name(self) -> str:
        return "faiss"

    def add(self, records: list[MemoryRecord]) -> list[str]:
        if not records:
            return []

        vectors = np.vstack([
            self.embedding_fn(record.text, self.embedding_dimension)
            for record in records
        ]).astype(np.float32)

        self._index.add(vectors)
        self._records.extend(records)
        return [record.record_id for record in records]

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        if not self._records or top_k <= 0:
            return []

        actual_k = min(top_k, len(self._records))
        query_vector = self.embedding_fn(query, self.embedding_dimension).reshape(1, -1).astype(np.float32)

        scores, indices = self._index.search(query_vector, actual_k)
        
        results: list[SearchResult] = []
        for position, score in zip(indices[0], scores[0]):
            if position < 0 or position >= len(self._records):
                continue
            record = self._records[int(position)]
            results.append(
                SearchResult(
                    record_id=record.record_id,
                    text=record.text,
                    label=record.label,
                    provenance=record.provenance,
                    score=round(float(score), 8),
                )
            )
        return results

    def count(self) -> int:
        return len(self._records)

    def clear(self) -> None:
        self._records = []
        self._init_index()
