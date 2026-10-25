"""Pinned sentence-transformer inference wrapper for local experiments."""

from __future__ import annotations

from typing import Any

import numpy as np


class SentenceTransformerEmbedder:
    """Run a fixed Sentence Transformers model locally and return unit vectors."""

    def __init__(
        self,
        model_name: str,
        revision: str,
        *,
        device: str = "cpu",
        local_files_only: bool = False,
        batch_size: int = 32,
    ) -> None:
        if not model_name or not revision:
            raise ValueError("model_name and immutable revision are required")
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as error:
            raise RuntimeError(
                "SentenceTransformer experiments require the 'research' extra; "
                "install with `python -m pip install -e .[dev,research]`."
            ) from error

        self.model_name = model_name
        self.revision = revision
        self.device = device
        self.batch_size = batch_size
        self._model: Any = SentenceTransformer(
            model_name,
            revision=revision,
            device=device,
            local_files_only=local_files_only,
        )
        dimension = self._model.get_embedding_dimension()
        if not dimension:
            raise RuntimeError(f"Model {model_name} did not report an embedding dimension")
        self.dimension = int(dimension)
        self._model.eval()

    @property
    def metadata(self) -> dict[str, str | int]:
        return {
            "kind": "sentence_transformer",
            "model_name": self.model_name,
            "model_revision": self.revision,
            "dimension": self.dimension,
            "device": self.device,
            "normalized": 1,
        }

    def encode(self, texts: list[str]) -> np.ndarray:
        if not texts:
            return np.empty((0, self.dimension), dtype=np.float32)
        vectors = self._model.encode(
            texts,
            batch_size=self.batch_size,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )
        result = np.asarray(vectors, dtype=np.float32)
        if result.shape != (len(texts), self.dimension):
            raise RuntimeError(f"Unexpected embedding shape: {result.shape}")
        if not np.isfinite(result).all():
            raise RuntimeError("Embedding model returned non-finite values")
        return result
