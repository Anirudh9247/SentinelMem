"""Backend adapters for SentinelMem memory systems."""

from sentinelmem.backends.base import BaseMemoryBackend, SearchResult
from sentinelmem.backends.faiss_backend import FAISSBackend
from sentinelmem.backends.langmem_backend import LangMemBackend
from sentinelmem.backends.mem0_backend import Mem0Backend
from sentinelmem.backends.registry import BackendRegistry

__all__ = [
    "BaseMemoryBackend",
    "SearchResult",
    "FAISSBackend",
    "Mem0Backend",
    "LangMemBackend",
    "BackendRegistry",
]
