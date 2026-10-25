# SentinelMem threat model and scope

## Intended research question

Can retrieval-time trust controls reduce exposure to poisoned memory in LLM agents across memory backends while preserving benign task utility? The current repository does not answer that question yet.

## Current prototype boundary

All checked-in scenarios use synthetic text. The FAISS real-embedding run uses a pinned sentence-transformer model locally; the hash fixture remains available. `EmulatedMem0Backend` and `EmulatedLangMemBackend` are local adapters, not the upstream libraries. The ReUI dashboard reads stored JSON and does not connect to a running experiment API.

The Python simulation inserts attack-labelled records directly and applies rule-based signals. There is no conversation agent, extraction loop, tool execution, or cross-agent memory path. MINJA/sleeper/direct-write are fixture labels and generators, not full attack reproductions. SQLite now offers persistence primitives for provenance, audit events, and quarantine, but the trust engine is not yet wired to enforce or review those records.

## In scope

- Synthetic memory poisoning scenarios and benign controls.
- Backend-agnostic retrieval governance as the research design target.
- Reproducible local experiments with stored configs and results.

## Out of scope for the current prototype

- External service targets, real user data, and live account credentials.
- Claims of production safety or protection against adaptive attackers.
- Evidence of behavior by Mem0, LangMem, LangGraph, or an LLM agent.

Remaining integration and evaluation work is tracked in [docs/carry-over.md](carry-over.md).
