"""FAISS vector database memory backend adapter."""

from __future__ import annotations

from typing import Any

import numpy as np

from sentinelmem.backends.base import BaseMemoryBackend, EmbeddingFn, SearchResult
from sentinelmem.embeddings import Embedder
from sentinelmem.models import MemoryRecord


class FAISSBackend(BaseMemoryBackend):
    """FAISS IndexFlat backend; embedding providers are injected and normalized."""

    def __init__(
        self,
        embedding_dimension: int | None = None,
        embedding_fn: EmbeddingFn | None = None,
        index_type: str = "FlatIP",
        *,
        embedder: Embedder | None = None,
        audit_ledger: Any | None = None,
    ) -> None:
        super().__init__(embedding_dimension, embedding_fn, embedder=embedder, audit_ledger=audit_ledger)
        self.index_type = index_type
        self._records: list[MemoryRecord] = []
        self._index: Any = None
        self._init_index()

    def _init_index(self) -> None:
        try:
            import faiss
        except ImportError as error:
            raise RuntimeError("faiss-cpu is required to use FAISSBackend; install project dependencies.") from error
        if self.index_type == "FlatIP":
            self._index = faiss.IndexFlatIP(self.embedding_dimension)
        elif self.index_type == "FlatL2":
            self._index = faiss.IndexFlatL2(self.embedding_dimension)
        else:
            raise ValueError(f"Unsupported FAISS index_type: {self.index_type}")

    @property
    def name(self) -> str:
        return "faiss"

    def _write_records(self, records: list[MemoryRecord]) -> list[str]:
        if not records:
            return []
        vectors = np.vstack([self.embedding_fn(record.text, self.embedding_dimension) for record in records]).astype(np.float32)
        if vectors.shape != (len(records), self.embedding_dimension):
            raise ValueError(f"Embedding shape {vectors.shape} does not match FAISS index dimension {self.embedding_dimension}")
        self._index.add(vectors)
        self._records.extend(records)
        return [record.record_id for record in records]

    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        if not self._records or top_k <= 0:
            return []
        scores, indices = self._index.search(
            self.embedding_fn(query, self.embedding_dimension).reshape(1, -1).astype(np.float32),
            min(top_k, len(self._records)),
        )
        results = []
        for position, score in zip(indices[0], scores[0]):
            if 0 <= position < len(self._records):
                record = self._records[int(position)]
                results.append(SearchResult(record.record_id, record.text, record.label, record.provenance, round(float(score), 8), record.metadata))
        return results

    def delete(self, record_id: str) -> bool:
        old_count = len(self._records)
        self._records = [record for record in self._records if record.record_id != record_id]
        if len(self._records) == old_count:
            return False
        self._init_index()
        if self._records:
            vectors = np.vstack([self.embedding_fn(record.text, self.embedding_dimension) for record in self._records]).astype(np.float32)
            self._index.add(vectors)
        return True

    def list(self) -> list[MemoryRecord]:
        return list(self._records)

    def count(self) -> int:
        return len(self._records)

    def clear(self) -> None:
        self._records = []
        self._init_index()
