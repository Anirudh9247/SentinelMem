"""Backend registry for dynamic instantiation of memory backends."""

from __future__ import annotations

from typing import Any, Type

from sentinelmem.backends.base import BaseMemoryBackend
from sentinelmem.backends.emulated_langmem_backend import EmulatedLangMemBackend
from sentinelmem.backends.emulated_mem0_backend import EmulatedMem0Backend
from sentinelmem.backends.faiss_backend import FAISSBackend


class BackendRegistry:
    """Registry of implemented adapters; emulators are named explicitly."""

    _backends: dict[str, Type[BaseMemoryBackend]] = {
        "faiss": FAISSBackend,
        "emulated_mem0": EmulatedMem0Backend,
        "emulated_langmem": EmulatedLangMemBackend,
    }

    @classmethod
    def register(cls, name: str, backend_cls: Type[BaseMemoryBackend]) -> None:
        cls._backends[name.lower()] = backend_cls

    @classmethod
    def get(cls, name: str, **kwargs: Any) -> BaseMemoryBackend:
        name_lower = name.lower()
        if name_lower not in cls._backends:
            available = ", ".join(sorted(cls._backends))
            raise ValueError(f"Unknown backend '{name}'. Available backends: {available}")
        return cls._backends[name_lower](**kwargs)

    @classmethod
    def list_available(cls) -> list[str]:
        return sorted(cls._backends)
