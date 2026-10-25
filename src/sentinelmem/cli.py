"""Command-line interface for synthetic SentinelMem prototype simulations."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from sentinelmem.evaluation.benchmark import run_experiment


def main() -> None:
    # Ensure UTF-8 output if supported
    if sys.stdout.encoding != "utf-8" and hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parser = argparse.ArgumentParser(
        description="Run a synthetic retrieval-and-filtering prototype simulation; this is not an agent security evaluation."
    )
    parser.add_argument(
        "--backend",
        choices=["faiss", "emulated_mem0", "emulated_langmem"],
        default="faiss",
        help="Prototype backend option (Mem0 and LangMem are local emulations).",
    )
    parser.add_argument(
        "--attack",
        choices=["minja", "sleeper", "direct_write"],
        default="minja",
        help="Payload fixture to simulate; these are not faithful attack reproductions.",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=3,
        help="Number of nearest memories to retrieve.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional path to write synthetic simulation output JSON.",
    )

    args = parser.parse_args()

    print("\n[SentinelMem] Running synthetic prototype simulation (not an empirical security benchmark)...")
    print(f"   * Backend:  {args.backend.upper()}")
    print(f"   * Attack:   {args.attack.upper()}")
    print(f"   * Top-k:    {args.top_k}")

    summary = run_experiment(
        backend_name=args.backend,
        attack_name=args.attack,
        top_k=args.top_k,
    )

    print("\n[Synthetic Fixture Summary — Not Research Measurements]")
    print("   +----------------------------------+--------------+")
    print(f"   | Unfiltered unsafe-query proxy    | {summary.unmitigated_asr * 100:>10.1f}% |")
    print(f"   | Post-filter unsafe-query proxy   | {summary.defended_asr * 100:>10.1f}% |")
    print(f"   | Fixture proportion difference    | {summary.defense_efficacy * 100:>10.1f}% |")
    print(f"   | Benign candidate rejection       | {summary.false_positive_rate * 100:>10.1f}% |")
    print(f"   | Prototype loop time              | {summary.latency_ms:>8.2f} ms |")
    print("   +----------------------------------+--------------+\n")

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(summary.to_dict(), indent=2), encoding="utf-8")
        print(f"[Export] Synthetic simulation output written to {args.output}")


if __name__ == "__main__":
    main()
