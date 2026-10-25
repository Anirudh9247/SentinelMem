"""Run a deterministic matrix over seeded synthetic query variants."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from sentinelmem.artifacts import write_artifact
from sentinelmem.baseline import create_embedder, load_config
from sentinelmem.evaluation.seed_matrix import run_seed_matrix


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("configs/faiss_seeded_sampling.json"))
    parser.add_argument("--seed-start", type=int, default=20260822)
    parser.add_argument("--repeats", type=int, default=20)
    parser.add_argument("--output", type=Path, default=Path("results/faiss_seeded_query_matrix.json"))
    args = parser.parse_args()
    if args.repeats < 1:
        parser.error("--repeats must be at least 1")

    config_bytes = args.config.read_bytes()
    config = load_config(args.config)
    config_hash = hashlib.sha256(config_bytes).hexdigest()
    seeds = range(args.seed_start, args.seed_start + args.repeats)
    result = run_seed_matrix(
        config,
        seeds,
        embedder=create_embedder(config),
        config_sha256=config_hash,
    )
    write_artifact(args.output, result)
    print(f"Wrote {result['seed_count']} seeded runs to {args.output}")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
