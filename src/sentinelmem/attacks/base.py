"""Base attack interface for SentinelMem memory poisoning evaluations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from sentinelmem.backends.base import BaseMemoryBackend
from sentinelmem.models import MemoryRecord, Query


class BaseAttack(ABC):
    """Abstract base class for all memory poisoning attack simulations."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Name of the attack vector."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Technical description of attack mechanism and threat surface."""
        ...

    @abstractmethod
    def generate_payloads(self) -> list[MemoryRecord]:
        """Generate poisoned memory records specific to this attack strategy."""
        ...

    @abstractmethod
    def generate_eval_queries(self) -> list[Query]:
        """Generate evaluation queries designed to trigger or evaluate retrieval of poisoned memories."""
        ...

    def execute(self, backend: BaseMemoryBackend) -> list[str]:
        """Inject poisoned memories into the target backend. Returns injected IDs."""
        payloads = self.generate_payloads()
        return backend.add(payloads)
