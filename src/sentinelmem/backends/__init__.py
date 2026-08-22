"""Backend adapters for SentinelMem memory systems."""

from sentinelmem.backends.base import BaseMemoryBackend, SearchResult
from sentinelmem.backends.faiss_backend import FAISSBackend
from sentinelmem.backends.registry import BackendRegistry

__all__ = [
    "BaseMemoryBackend",
    "SearchResult",
    "FAISSBackend",
    "BackendRegistry",
]
