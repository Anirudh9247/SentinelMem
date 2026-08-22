"""Command-line interface for running SentinelMem security experiments."""

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
        description="SentinelMem: Security evaluation of memory poisoning defenses in LLM agents."
    )
    parser.add_argument(
        "--backend",
        choices=["faiss", "mem0", "langmem"],
        default="faiss",
        help="Memory backend adapter to evaluate.",
    )
    parser.add_argument(
        "--attack",
        choices=["minja", "sleeper", "direct_write"],
        default="minja",
        help="Attack vector to simulate.",
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
        help="Optional path to write JSON benchmark results.",
    )

    args = parser.parse_args()

    print("\n[SentinelMem] Running Security Evaluation Experiment...")
    print(f"   * Backend:  {args.backend.upper()}")
    print(f"   * Attack:   {args.attack.upper()}")
    print(f"   * Top-k:    {args.top_k}")

    summary = run_experiment(
        backend_name=args.backend,
        attack_name=args.attack,
        top_k=args.top_k,
    )

    print("\n[Benchmark Summary Results]")
    print("   +---------------------------+--------------+")
    print(f"   | Unmitigated Baseline ASR  | {summary.unmitigated_asr * 100:>10.1f}% |")
    print(f"   | Defended SentinelMem ASR  | {summary.defended_asr * 100:>10.1f}% |")
    print(f"   | Defense Efficacy (dASR)   | {summary.defense_efficacy * 100:>10.1f}% |")
    print(f"   | False Positive Rate (FPR) | {summary.false_positive_rate * 100:>10.1f}% |")
    print(f"   | Evaluation Latency        | {summary.latency_ms:>8.2f} ms |")
    print("   +---------------------------+--------------+\n")

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(summary.to_dict(), indent=2), encoding="utf-8")
        print(f"[Export] Results successfully written to {args.output}")


if __name__ == "__main__":
    main()
