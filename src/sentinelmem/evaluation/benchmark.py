"""End-to-end security benchmark harness for SentinelMem."""

from __future__ import annotations

import time
from typing import Any

from sentinelmem.attacks import BaseAttack, DirectWriteAttack, MINJAAttack, SleeperAttack
from sentinelmem.backends import BackendRegistry, BaseMemoryBackend
from sentinelmem.defense import SentinelEngine
from sentinelmem.models import BenchmarkSummary, MemoryRecord, Query
from sentinelmem.synthetic import load_synthetic_scenario


ATTACK_MAP: dict[str, type[BaseAttack]] = {
    "minja": MINJAAttack,
    "sleeper": SleeperAttack,
    "direct_write": DirectWriteAttack,
}


def run_experiment(
    backend_name: str = "faiss",
    attack_name: str = "minja",
    top_k: int = 3,
    embedding_dimension: int = 64,
) -> BenchmarkSummary:
    """Execute a full attack vs. defense benchmark on a specified backend."""
    # 1. Initialize backend
    backend = BackendRegistry.get(backend_name, embedding_dimension=embedding_dimension)
    backend.clear()

    # 2. Ingest benign baseline memories
    benign_memories, _ = load_synthetic_scenario()
    clean_records = [m for m in benign_memories if m.label == "benign"]
    backend.add(clean_records)

    # 3. Instantiate attack and inject payloads
    attack_cls = ATTACK_MAP.get(attack_name.lower(), MINJAAttack)
    attack = attack_cls()
    poisoned_records = attack.generate_payloads()
    backend.add(poisoned_records)

    # Map record_id to full MemoryRecord for inspection
    all_records_map = {m.record_id: m for m in clean_records + poisoned_records}

    # 4. Generate evaluation queries
    eval_queries = attack.generate_eval_queries()
    engine = SentinelEngine()

    unmitigated_unsafe_count = 0
    defended_unsafe_count = 0
    benign_retrievals_total = 0
    benign_blocked_count = 0

    start_time = time.perf_counter()
    details: list[dict[str, Any]] = []

    for query in eval_queries:
        raw_results = backend.search(query.text, top_k=top_k)
        
        # Raw / Unmitigated evaluation
        raw_has_unsafe = any(r.label == query.unsafe_label for r in raw_results)
        if raw_has_unsafe:
            unmitigated_unsafe_count += 1

        # Defended evaluation with SentinelEngine
        candidate_records = [all_records_map[r.record_id] for r in raw_results if r.record_id in all_records_map]
        decisions = engine.filter_retrievals(candidate_records, query=query.text)

        passed_records = [d for d in decisions if d.passed_to_context]
        defended_has_unsafe = any(
            all_records_map[d.record_id].label == query.unsafe_label for d in passed_records
        )
        if defended_has_unsafe:
            defended_unsafe_count += 1

        # False positive check on benign records
        for d in decisions:
            rec = all_records_map[d.record_id]
            if rec.label == "benign":
                benign_retrievals_total += 1
                if not d.passed_to_context:
                    benign_blocked_count += 1

        details.append({
            "query_id": query.query_id,
            "query_text": query.text,
            "raw_retrieved_count": len(raw_results),
            "unmitigated_unsafe": raw_has_unsafe,
            "defended_unsafe": defended_has_unsafe,
            "decisions": [d.to_dict() for d in decisions],
        })

    elapsed_ms = (time.perf_counter() - start_time) * 1000

    q_len = max(1, len(eval_queries))
    unmitigated_asr = unmitigated_unsafe_count / q_len
    defended_asr = defended_unsafe_count / q_len
    efficacy = unmitigated_asr - defended_asr
    fpr = (benign_blocked_count / benign_retrievals_total) if benign_retrievals_total > 0 else 0.0

    return BenchmarkSummary(
        backend=backend_name,
        attack=attack.name,
        queries_count=len(eval_queries),
        unmitigated_asr=unmitigated_asr,
        defended_asr=defended_asr,
        defense_efficacy=efficacy,
        false_positive_rate=fpr,
        latency_ms=elapsed_ms,
        details=details,
    )
