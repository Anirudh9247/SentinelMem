"""Backend contracts, provenance stamping, and shared data structures."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field, replace
import hashlib
import time
from typing import Any, Callable

import numpy as np

from sentinelmem.embeddings import Embedder, HashEmbedder
from sentinelmem.models import MemoryRecord


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
    """Common interface for local memory stores and future real adapters."""

    def __init__(
        self,
        embedding_dimension: int | None = None,
        embedding_fn: EmbeddingFn | None = None,
        *,
        embedder: Embedder | None = None,
        audit_ledger: Any | None = None,
    ) -> None:
        if embedder is not None:
            if embedding_dimension is not None and embedding_dimension != embedder.dimension:
                raise ValueError("embedding_dimension must match the supplied embedder")
            embedding_dimension = embedder.dimension
        elif embedding_fn is None:
            embedder = HashEmbedder(embedding_dimension or 64)
            embedding_dimension = embedder.dimension
        elif embedding_dimension is None:
            embedding_dimension = 64
        if embedding_dimension is None or embedding_dimension <= 0:
            raise ValueError("embedding_dimension must be positive")
        self.embedding_dimension = embedding_dimension
        self.embedder = embedder
        self.embedding_fn = embedding_fn or self._embed_one
        self.audit_ledger = audit_ledger

    def _embed_one(self, text: str, dimension: int) -> np.ndarray:
        if self.embedder is None:
            raise RuntimeError("No embedding provider is configured")
        if self.embedder.dimension != dimension:
            raise ValueError("embedding dimension differs from the backend index")
        return self.embedder.encode([text])[0]

    def _stamp(self, record: MemoryRecord, session_id: str, agent_id: str) -> MemoryRecord:
        return replace(
            record,
            source=record.source or record.provenance,
            session_id=record.session_id or session_id,
            agent_id=record.agent_id or agent_id,
            written_at=time.time(),
            content_hash=hashlib.sha256(record.text.encode("utf-8")).hexdigest(),
        )

    @property
    @abstractmethod
    def name(self) -> str: ...

    def write(
        self,
        records: MemoryRecord | list[MemoryRecord],
        *,
        session_id: str = "default",
        agent_id: str = "sentinelmem",
    ) -> list[str]:
        """Write records after attaching an auditable source and content digest."""
        batch = [records] if isinstance(records, MemoryRecord) else records
        stamped = [self._stamp(record, session_id, agent_id) for record in batch]
        record_ids = self._write_records(stamped)
        if self.audit_ledger is not None:
            for record in stamped:
                self.audit_ledger.record_write(record)
        return record_ids

    def add(self, records: list[MemoryRecord]) -> list[str]:
        """Compatibility alias; new code should call `write`."""
        return self.write(records)

    @abstractmethod
    def _write_records(self, records: list[MemoryRecord]) -> list[str]: ...

    @abstractmethod
    def search(self, query: str, top_k: int = 3) -> list[SearchResult]: ...

    def search_batch(self, queries: list[str], top_k: int = 3) -> list[list[SearchResult]]:
        return [self.search(query, top_k=top_k) for query in queries]

    @abstractmethod
    def delete(self, record_id: str) -> bool: ...

    @abstractmethod
    def list(self) -> list[MemoryRecord]: ...

    def export_state(self) -> list[dict[str, Any]]:
        """Return backend-independent record data for local snapshots."""
        return [asdict(record) for record in self.list()]

    @abstractmethod
    def count(self) -> int: ...

    @abstractmethod
    def clear(self) -> None: ...

    def reset(self) -> None:
        """Reset the backend to an empty state."""
        self.clear()


MemoryBackend = BaseMemoryBackend
