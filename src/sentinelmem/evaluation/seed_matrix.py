"""Repeated seeded query-variant runs with descriptive summaries."""

from __future__ import annotations

import hashlib
import json
import statistics
from pathlib import Path
from typing import Any, Sequence

from sentinelmem.artifacts import ARTIFACT_SCHEMA_VERSION, runtime_versions, source_revision
from sentinelmem.baseline import create_embedder, run_baseline


def run_seed_matrix(
    config: dict[str, Any],
    seeds: Sequence[int],
    *,
    embedder: Any | None = None,
    config_sha256: str | None = None,
) -> dict[str, Any]:
    """Run the configured seeded sampler once for each supplied seed."""
    sampling = config.get("sampling", {})
    if sampling.get("protocol") != "stratified_query_variant_v1":
        raise ValueError("seed matrix requires stratified_query_variant_v1 sampling")
    if not seeds:
        raise ValueError("at least one seed is required")
    normalized_seeds = [int(seed) for seed in seeds]
    if len(set(normalized_seeds)) != len(normalized_seeds):
        raise ValueError("seeds must be unique")

    shared_embedder = embedder or create_embedder(config)
    runs: list[dict[str, Any]] = []
    for seed in normalized_seeds:
        run_config = {**config, "seed": seed}
        effective_hash = hashlib.sha256(
            json.dumps(run_config, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        result = run_baseline(
            run_config,
            embedder=shared_embedder,
            config_sha256=effective_hash,
        )
        runs.append({
            "seed": seed,
            "config_sha256": effective_hash,
            "metrics": result["metrics"],
            "sampling": result["sampling"],
            "cases": result["cases"],
            "timings": result["timings"],
        })

    rates = [float(run["metrics"]["unsafe_retrieval_rate"]) for run in runs]
    all_queries = [
        selected["query_id"]
        for run in runs
        for selected in run["sampling"]["selected_queries"]
    ]
    total_queries = sum(int(run["metrics"]["query_count"]) for run in runs)
    unsafe_count = sum(int(run["metrics"]["unsafe_retrieval_count"]) for run in runs)
    return {
        "schema_version": ARTIFACT_SCHEMA_VERSION,
        "benchmark": "faiss_seeded_query_variant_matrix",
        "config_template": config,
        "config_template_sha256": config_sha256,
        "source": source_revision(Path(__file__).resolve().parents[2]),
        "versions": runtime_versions(),
        "seed_count": len(runs),
        "total_query_samples": total_queries,
        "unique_query_variants_observed": len(set(all_queries)),
        "summary": {
            "pooled_unsafe_retrieval_count": unsafe_count,
            "pooled_query_count": total_queries,
            "pooled_unsafe_retrieval_rate": round(unsafe_count / total_queries, 6),
            "mean_per_seed_rate": round(statistics.fmean(rates), 6),
            "population_stddev_per_seed_rate": round(statistics.pstdev(rates), 6),
            "min_per_seed_rate": min(rates),
            "max_per_seed_rate": max(rates),
            "interval": None,
            "interpretation": (
                "Descriptive variation across deterministic samples from the finite "
                "synthetic query-variant pool; not a defense or attack success estimate."
            ),
        },
        "runs": runs,
    }
