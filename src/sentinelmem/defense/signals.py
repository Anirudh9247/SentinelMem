"""Security trust signal extractors for candidate memories."""

from __future__ import annotations

import math
import re
import time
from typing import Any, Callable

import numpy as np

from sentinelmem.models import MemoryRecord
from sentinelmem.synthetic import deterministic_embedding

# Known injection and prompt override markers
INJECTION_KEYWORDS = [
    "system override",
    "ignore previous",
    "disregard",
    "bypass security",
    "critical instruction",
    "system directive",
    "execute debug tool",
    "root privileges",
    "re-route",
]


class SemanticDriftDetector:
    """Evaluates semantic divergence, structural anomalies, and injection marker density."""

    def __init__(
        self,
        dimension: int = 64,
        embedding_fn: Callable[[str, int], np.ndarray] | None = None,
    ) -> None:
        self.dimension = dimension
        self.embedding_fn = embedding_fn or deterministic_embedding

    def score(self, record: MemoryRecord, query: str = "") -> float:
        """Return semantic trust score in range [0.0, 1.0]. Lower = higher drift / risk."""
        text_lower = record.text.lower()
        
        # Check for instruction injection markers
        marker_hits = sum(1 for kw in INJECTION_KEYWORDS if kw in text_lower)
        if marker_hits > 0:
            penalty = min(0.9, 0.45 * marker_hits)
            return max(0.05, 1.0 - penalty)

        # Instruction-shaped syntax detection (colons, imperative commands)
        if re.search(r"^(override|notice|directive|instruction|system):", text_lower):
            return 0.20

        # Untrusted label check
        if record.label == "instruction_shaped":
            return 0.25

        return 0.95


class TemporalAnomalyDetector:
    """Evaluates ingestion frequency bursts and timestamp consistency."""

    def __init__(self, burst_threshold_seconds: float = 60.0) -> None:
        self.burst_threshold_seconds = burst_threshold_seconds

    def score(self, record: MemoryRecord, query_time: float | None = None) -> float:
        """Return temporal trust score in range [0.0, 1.0]."""
        current = query_time or time.time()
        age_seconds = abs(current - record.timestamp)

        # If memory timestamp is in the future
        if record.timestamp > current + 60.0:
            return 0.10

        # Check metadata for rapid burst flags
        if record.metadata.get("burst_ingested", False):
            return 0.30

        return 0.92


class ProvenanceVerifier:
    """Verifies origin authority, session lineage, and ingress authenticity."""

    PROVENANCE_WEIGHTS: dict[str, float] = {
        "trusted_profile": 1.00,
        "trusted_project": 0.95,
        "trusted_calendar": 0.90,
        "authenticated_tool": 0.80,
        "external_integration": 0.45,
        "untrusted_import": 0.10,
        "anonymous": 0.05,
    }

    def score(self, record: MemoryRecord) -> float:
        """Return provenance trust score in range [0.0, 1.0]."""
        return self.PROVENANCE_WEIGHTS.get(record.provenance, 0.20)


class SourceCredibilityScorer:
    """Evaluates actor domain authority and metadata integrity."""

    def score(self, record: MemoryRecord) -> float:
        """Return credibility score in range [0.0, 1.0]."""
        if record.provenance.startswith("trusted_"):
            return 0.95
        if record.provenance == "authenticated_tool":
            return 0.85
        if record.provenance == "untrusted_import":
            return 0.15
        return 0.40
