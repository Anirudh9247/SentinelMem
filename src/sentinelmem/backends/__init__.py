"""Backend adapters for SentinelMem memory systems."""

from sentinelmem.backends.base import BaseMemoryBackend, MemoryBackend, SearchResult
from sentinelmem.backends.emulated_langmem_backend import EmulatedLangMemBackend
from sentinelmem.backends.emulated_mem0_backend import EmulatedMem0Backend
from sentinelmem.backends.faiss_backend import FAISSBackend
from sentinelmem.backends.registry import BackendRegistry

__all__ = [
    "BaseMemoryBackend",
    "MemoryBackend",
    "SearchResult",
    "FAISSBackend",
    "EmulatedMem0Backend",
    "EmulatedLangMemBackend",
    "BackendRegistry",
]
