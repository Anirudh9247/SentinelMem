"""SentinelEngine: Multi-signal trust fusion and retrieval-time policy enforcement."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sentinelmem.defense.signals import (
    ProvenanceVerifier,
    SemanticDriftDetector,
    SourceCredibilityScorer,
    TemporalAnomalyDetector,
)
from sentinelmem.models import DecisionType, DefenseDecision, MemoryRecord, TrustBreakdown


@dataclass
class EngineConfig:
    """Weights and decision threshold configuration for SentinelEngine."""

    weight_semantic: float = 0.35
    weight_temporal: float = 0.15
    weight_provenance: float = 0.30
    weight_credibility: float = 0.20

    allow_threshold: float = 0.75
    flag_threshold: float = 0.50
    block_threshold: float = 0.30

    def __post_init__(self) -> None:
        total = self.weight_semantic + self.weight_temporal + self.weight_provenance + self.weight_credibility
        if not (0.99 <= total <= 1.01):
            raise ValueError(f"Signal weights must sum to 1.0 (got {total})")


class SentinelEngine:
    """Retrieval-time defense engine that scores and gates candidate memory records."""

    def __init__(self, config: EngineConfig | None = None) -> None:
        self.config = config or EngineConfig()
        self.semantic_detector = SemanticDriftDetector()
        self.temporal_detector = TemporalAnomalyDetector()
        self.provenance_verifier = ProvenanceVerifier()
        self.credibility_scorer = SourceCredibilityScorer()

    def evaluate_trust(self, record: MemoryRecord, query: str = "") -> TrustBreakdown:
        """Compute individual and composite trust scores for a memory record."""
        s_drift = self.semantic_detector.score(record, query=query)
        s_temp = self.temporal_detector.score(record)
        s_prov = self.provenance_verifier.score(record)
        s_cred = self.credibility_scorer.score(record)

        composite = (
            self.config.weight_semantic * s_drift
            + self.config.weight_temporal * s_temp
            + self.config.weight_provenance * s_prov
            + self.config.weight_credibility * s_cred
        )

        return TrustBreakdown(
            semantic_drift=s_drift,
            temporal_anomaly=s_temp,
            provenance_score=s_prov,
            source_credibility=s_cred,
            composite_score=composite,
        )

    def inspect_record(self, record: MemoryRecord, query: str = "") -> DefenseDecision:
        """Evaluate memory record and issue a retrieval policy decision."""
        trust = self.evaluate_trust(record, query=query)
        score = trust.composite_score

        if score >= self.config.allow_threshold:
            return DefenseDecision(
                record_id=record.record_id,
                text=record.text,
                decision=DecisionType.ALLOW,
                trust=trust,
                passed_to_context=True,
                reason="High trust across semantic, temporal, and provenance signals.",
            )
        elif score >= self.config.flag_threshold:
            return DefenseDecision(
                record_id=record.record_id,
                text=record.text,
                decision=DecisionType.FLAG,
                trust=trust,
                passed_to_context=True,
                annotation="[SECURITY NOTICE: UNVERIFIED CONTEXT]",
                reason="Moderate trust score; flagged for agent caution.",
            )
        elif score >= self.config.block_threshold:
            return DefenseDecision(
                record_id=record.record_id,
                text=record.text,
                decision=DecisionType.QUARANTINE,
                trust=trust,
                passed_to_context=False,
                reason="Low trust; suspicious provenance or instruction pattern quarantined.",
            )
        else:
            return DefenseDecision(
                record_id=record.record_id,
                text=record.text,
                decision=DecisionType.BLOCK,
                trust=trust,
                passed_to_context=False,
                reason="Critical trust failure; malicious injection markers detected.",
            )

    def filter_retrievals(
        self, records: list[MemoryRecord], query: str = ""
    ) -> list[DefenseDecision]:
        """Inspect and filter a batch of candidate retrieved memories."""
        return [self.inspect_record(rec, query=query) for rec in records]
