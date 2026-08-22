"""Backend registry for dynamic instantiation of memory backends."""

from __future__ import annotations

from typing import Any, Type
from sentinelmem.backends.base import BaseMemoryBackend
from sentinelmem.backends.faiss_backend import FAISSBackend
from sentinelmem.backends.langmem_backend import LangMemBackend
from sentinelmem.backends.mem0_backend import Mem0Backend


class BackendRegistry:
    """Registry allowing backends to be registered and instantiated by name."""

    _backends: dict[str, Type[BaseMemoryBackend]] = {
        "faiss": FAISSBackend,
        "mem0": Mem0Backend,
        "langmem": LangMemBackend,
    }

    @classmethod
    def register(cls, name: str, backend_cls: Type[BaseMemoryBackend]) -> None:
        """Register a new backend adapter class."""
        cls._backends[name.lower()] = backend_cls

    @classmethod
    def get(cls, name: str, **kwargs: Any) -> BaseMemoryBackend:
        """Instantiate a backend adapter by name."""
        name_lower = name.lower()
        if name_lower not in cls._backends:
            available = ", ".join(sorted(cls._backends.keys()))
            raise ValueError(f"Unknown backend '{name}'. Available backends: {available}")
        return cls._backends[name_lower](**kwargs)

    @classmethod
    def list_available(cls) -> list[str]:
        """List all registered backend names."""
        return sorted(cls._backends.keys())
