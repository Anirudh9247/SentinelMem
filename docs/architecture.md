# SentinelMem architecture and implementation status

SentinelMem is a synthetic research prototype. The only connected vector backend is local FAISS; Mem0 and LangMem remain explicitly named emulations. No LLM agent is connected.

## Current data flow

```text
Synthetic records and queries
        │
        ├── HashEmbedder (fixture only)
        └── Pinned SentenceTransformerEmbedder (local inference)
                    │
                    ▼
          FAISSBackend / MemoryBackend
                    │
          optional SQLiteLedger
       provenance + audit + quarantine
                    │
                    ▼
           Versioned JSON artifact
                    │
                    ▼
          Static ReUI research console
```

The real embedding path uses `sentence-transformers/all-MiniLM-L6-v2` from the immutable revision in `configs/faiss_baseline.json`. It embeds fixed synthetic text and does not measure agent behavior.

## Backend contract

`BaseMemoryBackend` (also exported as `MemoryBackend`) provides `write`, `search`, `delete`, `list`, `export_state`, and `reset`; `add` and `clear` remain compatibility aliases. Public writes stamp source, session ID, agent ID, write timestamp, and SHA-256 content digest. The optional `SQLiteLedger` persists provenance and audit events.

- `FAISSBackend` uses `IndexFlatIP` by default and supports injected embedding providers. The research baseline injects the pinned sentence-transformer model.
- `EmulatedMem0Backend` and `EmulatedLangMemBackend` are local NumPy-backed fixtures. They do not call the upstream libraries.

## Artifacts and UI

`sentinelmem.baseline` writes schema-v2 JSON containing the input config/hash, seed, package versions, source revision and dirty state, embedding identity, corpus summary, deterministic metrics, timings, and per-query retrieval records. Timings are separated because wall-clock latency is environment-dependent.

The ReUI app imports a result artifact at build time. It is a static artifact viewer, not a live API or control plane. The standalone `index.html` demo remains an independent browser-only illustration.

## Persistent storage boundary

SQLite storage supports write provenance, an append-only audit event table with a verifiable hash chain, and persisted quarantine records. It is exercised by tests and `scripts/manual_storage_check.py`. The current `SentinelEngine` does not yet route decisions into the quarantine store or create these audit events automatically; that enforcement/review integration remains in the planned defense sprint.

## Not yet implemented

Real Mem0 and LangMem adapters, agent harnesses, faithful attack paths and success oracles, retrieval-time enforcement, a quarantine review/release workflow, adaptive attacks, matrix orchestration, repeated cross-backend evaluation, ablations, and confidence intervals remain on the project plan in [docs/carry-over.md](carry-over.md).
