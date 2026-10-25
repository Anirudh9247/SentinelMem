"""Run a synthetic retrieval baseline with a selected embedding provider."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from time import perf_counter
from typing import Any


from sentinelmem.artifacts import ARTIFACT_SCHEMA_VERSION, runtime_versions, source_revision, write_artifact
from sentinelmem.backends.faiss_backend import FAISSBackend
from sentinelmem.embeddings import HashEmbedder, SentenceTransformerEmbedder
from sentinelmem.synthetic import load_seeded_query_variant_scenario, load_synthetic_scenario


def load_config(config_path: Path) -> dict[str, Any]:
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    required = {"schema_version", "seed", "top_k", "scenario", "embedding"}
    missing = required.difference(config)
    if missing:
        raise ValueError(f"configuration missing fields: {', '.join(sorted(missing))}")
    return config


def create_embedder(config: dict[str, Any]):
    embedding_config = config["embedding"]
    kind = embedding_config.get("kind")
    if kind == "deterministic_hash_stub":
        return HashEmbedder(int(embedding_config.get("dimension", 64)))
    if kind == "sentence_transformer":
        return SentenceTransformerEmbedder(
            model_name=embedding_config["model_name"],
            revision=embedding_config["revision"],
            device=embedding_config.get("device", "cpu"),
            local_files_only=bool(embedding_config.get("local_files_only", False)),
        )
    raise ValueError(f"Unsupported embedding kind: {kind!r}")


def run_baseline(config: dict[str, Any], *, embedder: Any | None = None, config_sha256: str | None = None) -> dict[str, Any]:
    """Run FAISS retrieval using the fixed or opt-in seeded synthetic protocol."""
    seed = int(config["seed"])
    embedding = embedder or create_embedder(config)
    top_k = int(config["top_k"])
    sampling_config = config.get("sampling")
    if sampling_config is None:
        memories, queries = load_synthetic_scenario()
        sampling_metadata = {
            "protocol": "fixed_scenario_v1",
            "selected_queries": [
                {"query_id": query.query_id, "text": query.text} for query in queries
            ],
        }
    else:
        protocol = sampling_config.get("protocol")
        if protocol != "stratified_query_variant_v1":
            raise ValueError(f"Unsupported sampling protocol: {protocol!r}")
        variants_per_family = int(sampling_config.get("variants_per_family", 1))
        memories, queries, sampling_metadata = load_seeded_query_variant_scenario(
            seed, variants_per_family=variants_per_family
        )
    if not 0 < top_k <= len(memories):
        raise ValueError("top_k must be between 1 and the corpus size")

    backend = FAISSBackend(embedder=embedding)
    backend.write(memories, session_id=f"baseline-{seed}", agent_id="baseline-runner")
    started = perf_counter()
    batch_results = backend.search_batch([query.text for query in queries], top_k=top_k)
    elapsed_ms = (perf_counter() - started) * 1000

    cases = []
    unsafe_retrievals = 0
    for query, results in zip(queries, batch_results):
        unsafe = any(result.label == query.unsafe_label for result in results)
        unsafe_retrievals += int(unsafe)
        cases.append({
            "query_id": query.query_id,
            "query_text": query.text,
            "unsafe_retrieval": unsafe,
            "retrieved": [
                {"record_id": result.record_id, "label": result.label, "score": round(float(result.score), 8)}
                for result in results
            ],
        })

    project_root = Path(__file__).resolve().parents[2]
    artifact: dict[str, Any] = {
        "schema_version": ARTIFACT_SCHEMA_VERSION,
        "benchmark": "faiss_synthetic_retrieval_baseline",
        "scenario": config["scenario"],
        "seed": seed,
        "config": config,
        "config_sha256": config_sha256,
        "source": source_revision(project_root),
        "versions": runtime_versions(),
        "embedding": dict(embedding.metadata),
        "sampling": sampling_metadata,
        "corpus": {
            "records": len(memories),
            "untrusted_records": sum(memory.label == "instruction_shaped" for memory in memories),
        },
        "metrics": {
            "query_count": len(queries),
            "top_k": top_k,
            "unsafe_retrieval_count": unsafe_retrievals,
            "unsafe_retrieval_rate": round(unsafe_retrievals / len(queries), 6),
            "retrieved_record_count": sum(len(case["retrieved"]) for case in cases),
        },
        "timings": {"retrieval_latency_ms": round(elapsed_ms, 6)},
        "cases": cases,
    }
    return artifact


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/faiss_baseline.json"))
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()

    config_bytes = arguments.config.read_bytes()
    config = json.loads(config_bytes.decode("utf-8-sig"))
    required = {"schema_version", "seed", "top_k", "scenario", "embedding"}
    missing = required.difference(config)
    if missing:
        raise ValueError(f"configuration missing fields: {', '.join(sorted(missing))}")
    config_hash = hashlib.sha256(config_bytes).hexdigest()
    result = run_baseline(config, config_sha256=config_hash)
    default_name = "faiss_sentence_transformer.json" if config["embedding"]["kind"] == "sentence_transformer" else "faiss_hash_fixture_v2.json"
    output = arguments.output or Path("results") / default_name
    write_artifact(output, result)
    print(f"Wrote schema {ARTIFACT_SCHEMA_VERSION} baseline result to {output}")
    print(json.dumps(result["metrics"], sort_keys=True))


if __name__ == "__main__":
    main()
