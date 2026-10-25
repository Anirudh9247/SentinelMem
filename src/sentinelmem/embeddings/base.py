"""Pluggable, normalized vector encoders used by SentinelMem."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

import numpy as np


@runtime_checkable
class Embedder(Protocol):
    """Minimal encoder contract shared by FAISS and experiment runners."""

    dimension: int

    @property
    def metadata(self) -> dict[str, str | int]: ...

    def encode(self, texts: list[str]) -> np.ndarray: ...


class HashEmbedder:
    """Deterministic non-semantic stand-in retained for tests and fixtures."""

    def __init__(self, dimension: int = 64) -> None:
        if dimension <= 0:
            raise ValueError("dimension must be positive")
        self.dimension = dimension

    @property
    def metadata(self) -> dict[str, str | int]:
        return {"kind": "deterministic_hash_stub", "dimension": self.dimension}

    def encode(self, texts: list[str]) -> np.ndarray:
        from sentinelmem.synthetic import deterministic_embedding

        if not texts:
            return np.empty((0, self.dimension), dtype=np.float32)
        return np.vstack([deterministic_embedding(text, self.dimension) for text in texts]).astype(np.float32)
