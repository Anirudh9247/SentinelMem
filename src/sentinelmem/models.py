"""Core data models and type definitions for SentinelMem."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
import hashlib
import time
from typing import Any


class DecisionType(str, Enum):
    """Retrieval-time defense decision outcomes."""

    ALLOW = "ALLOW"
    FLAG = "FLAG"
    QUARANTINE = "QUARANTINE"
    BLOCK = "BLOCK"


@dataclass(frozen=True)
class MemoryRecord:
    """Standardized record with optional write-time provenance metadata."""

    record_id: str
    text: str
    label: str = "benign"
    provenance: str = "trusted_profile"
    timestamp: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)
    source: str | None = None
    session_id: str | None = None
    agent_id: str | None = None
    written_at: float | None = None
    content_hash: str | None = None

    def computed_content_hash(self) -> str:
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class Query:
    """Standardized retrieval query case."""

    query_id: str
    text: str
    unsafe_label: str = "instruction_shaped"


@dataclass(frozen=True)
class TrustBreakdown:
    """Individual security signal scores and composite score for a memory candidate."""

    semantic_drift: float
    temporal_anomaly: float
    provenance_score: float
    source_credibility: float
    composite_score: float

    def to_dict(self) -> dict[str, float]:
        return {
            "semantic_drift": round(self.semantic_drift, 4),
            "temporal_anomaly": round(self.temporal_anomaly, 4),
            "provenance_score": round(self.provenance_score, 4),
            "source_credibility": round(self.source_credibility, 4),
            "composite_score": round(self.composite_score, 4),
        }


@dataclass(frozen=True)
class DefenseDecision:
    """Final policy decision and audit trace for a candidate memory."""

    record_id: str
    text: str
    decision: DecisionType
    trust: TrustBreakdown
    passed_to_context: bool
    annotation: str = ""
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "record_id": self.record_id,
            "decision": self.decision.value,
            "passed_to_context": self.passed_to_context,
            "annotation": self.annotation,
            "reason": self.reason,
            "trust": self.trust.to_dict(),
        }


@dataclass
class BenchmarkSummary:
    """Synthetic retrieval-and-filtering proxy counters."""

    backend: str
    attack: str
    queries_count: int
    unmitigated_asr: float
    defended_asr: float
    defense_efficacy: float
    false_positive_rate: float
    latency_ms: float
    details: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "backend": self.backend,
            "attack": self.attack,
            "queries_count": self.queries_count,
            "unmitigated_asr": round(self.unmitigated_asr, 4),
            "defended_asr": round(self.defended_asr, 4),
            "defense_efficacy": round(self.defense_efficacy, 4),
            "false_positive_rate": round(self.false_positive_rate, 4),
            "latency_ms": round(self.latency_ms, 3),
            "details": self.details,
        }
