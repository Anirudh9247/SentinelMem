"""Versioned baseline artifact and deterministic result tests."""



def test_hash_fixture_baseline_has_versioned_reproducible_metrics():
    config = {
        "schema_version": "2.1",
        "seed": 17,
        "top_k": 3,
        "scenario": "synthetic_instruction_shaped_memory_v1",
        "embedding": {"kind": "deterministic_hash_stub", "dimension": 64},
    }
    first = run_baseline(config, embedder=HashEmbedder(64), config_sha256="fixture")
    second = run_baseline(config, embedder=HashEmbedder(64), config_sha256="fixture")
    assert first["schema_version"] == "2.1"
    assert first["metrics"] == second["metrics"]
    assert first["cases"] == second["cases"]
    assert first["embedding"]["kind"] == "deterministic_hash_stub"
    assert first["versions"]["numpy"]
    assert "commit" in first["source"]
    assert "retrieval_latency_ms" in first["timings"]
from sentinelmem.baseline import run_baseline
from sentinelmem.embeddings import HashEmbedder
from sentinelmem.evaluation.seed_matrix import run_seed_matrix


def _seeded_config():
    return {
        "schema_version": "2.1",
        "seed": 17,
        "top_k": 3,
        "scenario": "synthetic_instruction_shaped_memory_query_variants_v1",
        "sampling": {"protocol": "stratified_query_variant_v1", "variants_per_family": 1},
        "embedding": {"kind": "deterministic_hash_stub", "dimension": 64},
    }


def test_seeded_query_variant_run_is_reproducible_and_seed_sensitive():
    config = _seeded_config()
    first = run_baseline(config, embedder=HashEmbedder(64), config_sha256="fixture")
    repeated = run_baseline(config, embedder=HashEmbedder(64), config_sha256="fixture")
    other_config = {**config, "seed": 18}
    other = run_baseline(other_config, embedder=HashEmbedder(64), config_sha256="fixture")

    assert first["schema_version"] == "2.1"
    assert first["sampling"]["protocol"] == "stratified_query_variant_v1"
    assert first["sampling"]["selected_queries"] == repeated["sampling"]["selected_queries"]
    assert first["cases"] == repeated["cases"]
    assert first["sampling"]["selected_queries"] != other["sampling"]["selected_queries"]
    assert all(case["query_text"] for case in first["cases"])


def test_seed_matrix_summarizes_each_seed_and_query_sample():
    matrix = run_seed_matrix(
        _seeded_config(),
        [17, 18, 19],
        embedder=HashEmbedder(64),
        config_sha256="template",
    )

    assert matrix["seed_count"] == 3
    assert matrix["total_query_samples"] == 12
    assert matrix["summary"]["pooled_query_count"] == 12
    assert len(matrix["runs"]) == 3
    assert matrix["summary"]["interval"] is None
    assert matrix["unique_query_variants_observed"] > 4

def test_fixed_control_keeps_same_queries_across_seeds():
    config = _seeded_config()
    config.pop("sampling")
    first = run_baseline(config, embedder=HashEmbedder(64), config_sha256="fixture")
    second = run_baseline(
        {**config, "seed": 18},
        embedder=HashEmbedder(64),
        config_sha256="fixture",
    )

    assert [case["query_text"] for case in first["cases"]] == [
        case["query_text"] for case in second["cases"]
    ]
    assert first["metrics"] == second["metrics"]
    assert first["cases"] == second["cases"]
