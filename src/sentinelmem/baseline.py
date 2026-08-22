"""Run the first deterministic FAISS retrieval baseline."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from time import perf_counter
from typing import Any

import numpy as np

from sentinelmem.synthetic import deterministic_embedding, load_synthetic_scenario


def load_config(config_path: Path) -> dict[str, Any]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    required = {"schema_version", "seed", "embedding_dimension", "top_k", "scenario"}
    missing = required.difference(config)
    if missing:
        raise ValueError(f"configuration missing fields: {', '.join(sorted(missing))}")
    return config


def run_baseline(config: dict[str, Any]) -> dict[str, Any]:
    """Index the synthetic corpus and report unsafe-retrieval rate and latency."""
    try:
        import faiss
    except ImportError as error:
        raise RuntimeError("faiss-cpu is required; install the project dependencies first.") from error

    dimension = int(config["embedding_dimension"])
    top_k = int(config["top_k"])
    memories, queries = load_synthetic_scenario()
    if not 0 < top_k <= len(memories):
        raise ValueError("top_k must be between 1 and the corpus size")

    vectors = np.vstack([deterministic_embedding(memory.text, dimension) for memory in memories])
    index = faiss.IndexFlatIP(dimension)
    index.add(vectors)

    query_vectors = np.vstack([deterministic_embedding(query.text, dimension) for query in queries])
    started = perf_counter()
    scores, indices = index.search(query_vectors, top_k)
    elapsed_ms = (perf_counter() - started) * 1000

    cases = []
    unsafe_retrievals = 0
    for query, row_indices, row_scores in zip(queries, indices, scores):
        retrieved = [memories[int(position)] for position in row_indices]
        unsafe = any(record.label == query.unsafe_label for record in retrieved)
        unsafe_retrievals += int(unsafe)
        cases.append({
            "query_id": query.query_id,
            "unsafe_retrieval": unsafe,
            "retrieved": [
                {"record_id": record.record_id, "label": record.label, "score": round(float(score), 8)}
                for record, score in zip(retrieved, row_scores)
            ],
        })

    return {
        "schema_version": "1.0",
        "benchmark": "faiss_synthetic_retrieval_baseline",
        "scenario": config["scenario"],
        "seed": config["seed"],
        "embedding": {"kind": "deterministic_hash_stub", "dimension": dimension},
        "corpus": {"records": len(memories), "untrusted_records": sum(m.label == "instruction_shaped" for m in memories)},
        "metrics": {
            "queries": len(queries),
            "top_k": top_k,
            "unsafe_retrieval_rate": round(unsafe_retrievals / len(queries), 6),
            "retrieval_latency_ms": round(elapsed_ms, 6),
        },
        "cases": cases,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/faiss_baseline.json"))
    parser.add_argument("--output", type=Path, default=Path("results/faiss_baseline.json"))
    arguments = parser.parse_args()

    config = load_config(arguments.config)
    result = run_baseline(config)
    result["config_sha256"] = hashlib.sha256(arguments.config.read_bytes()).hexdigest()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote baseline result to {arguments.output}")


if __name__ == "__main__":
    main()
