"""Tests for SentinelMem data models."""

from sentinelmem.models import DecisionType, DefenseDecision, MemoryRecord, Query, TrustBreakdown


def test_memory_record_creation():
    rec = MemoryRecord(
        record_id="rec_01",
        text="Sample memory text",
        label="benign",
        provenance="trusted_profile",
    )
    assert rec.record_id == "rec_01"
    assert rec.label == "benign"
    assert rec.provenance == "trusted_profile"


def test_trust_breakdown_and_decision():
    trust = TrustBreakdown(
        semantic_drift=0.90,
        temporal_anomaly=0.85,
        provenance_score=0.95,
        source_credibility=0.90,
        composite_score=0.905,
    )
    decision = DefenseDecision(
        record_id="rec_01",
        text="Sample memory text",
        decision=DecisionType.ALLOW,
        trust=trust,
        passed_to_context=True,
    )
    assert decision.decision == DecisionType.ALLOW
    assert decision.passed_to_context is True
    d_dict = decision.to_dict()
    assert d_dict["decision"] == "ALLOW"
    assert d_dict["trust"]["composite_score"] == 0.905
