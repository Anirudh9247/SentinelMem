"""Tests for SentinelMem benchmark and experiment harness."""

from sentinelmem.evaluation import run_experiment


def test_benchmark_run_faiss_minja():
    summary = run_experiment(backend_name="faiss", attack_name="minja", top_k=3)
    assert summary.backend == "faiss"
    assert summary.queries_count > 0
    assert summary.unmitigated_asr >= summary.defended_asr
    assert summary.defense_efficacy >= 0.0
    assert summary.false_positive_rate < 0.20


def test_benchmark_run_mem0_and_langmem():
    summary_mem0 = run_experiment(backend_name="mem0", attack_name="minja", top_k=3)
    assert summary_mem0.backend == "mem0"
    assert summary_mem0.unmitigated_asr >= summary_mem0.defended_asr

    summary_langmem = run_experiment(backend_name="langmem", attack_name="sleeper", top_k=3)
    assert summary_langmem.backend == "langmem"
    assert summary_langmem.unmitigated_asr >= summary_langmem.defended_asr
