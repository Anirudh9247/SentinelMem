"""Abstract base classes and data contracts for SentinelMem memory backends."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np

from sentinelmem.synthetic import MemoryRecord, deterministic_embedding


@dataclass(frozen=True)
class SearchResult:
    """Standardized retrieval result returned by all memory backends."""

    record_id: str
    text: str
    label: str
    provenance: str
    score: float
    metadata: dict[str, Any] = field(default_factory=dict)


EmbeddingFn = Callable[[str, int], np.ndarray]


class BaseMemoryBackend(ABC):
    """Abstract interface that all memory backend adapters (FAISS, Mem0, LangMem) must implement."""

    def __init__(self, embedding_dimension: int = 64, embedding_fn: EmbeddingFn | None = None) -> None:
        if embedding_dimension <= 0:
            raise ValueError("embedding_dimension must be positive")
        self.embedding_dimension = embedding_dimension
        self.embedding_fn = embedding_fn or deterministic_embedding

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique identifier for the backend adapter (e.g., 'faiss', 'mem0', 'langmem')."""
        ...

    @abstractmethod
    def add(self, records: list[MemoryRecord]) -> list[str]:
        """Ingest memory records into the backend. Returns list of ingested record IDs."""
        ...

    @abstractmethod
    def search(self, query: str, top_k: int = 3) -> list[SearchResult]:
        """Search the backend for the top-k most relevant memories for a given query text."""
        ...

    def search_batch(self, queries: list[str], top_k: int = 3) -> list[list[SearchResult]]:
        """Batch query search. Default implementation calls search sequentially."""
        return [self.search(q, top_k=top_k) for q in queries]

    @abstractmethod
    def count(self) -> int:
        """Return the number of stored memory records in the backend."""
        ...

    @abstractmethod
    def clear(self) -> None:
        """Clear all stored memories and reset the index/storage."""
        ...
