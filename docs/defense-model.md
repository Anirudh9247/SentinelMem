# SentinelMem prototype trust heuristics and policy

The current engine in `src/sentinelmem/defense/` uses fixed, deterministic heuristic checks. The weights and thresholds are prototype settings, not calibrated security parameters.

## Current signals and decisions

| Signal | Current implementation |
|---|---|
| Semantic score | Marker strings, a prefix regex, the `instruction_shaped` fixture label, or a benign default. The score does not use sentence embeddings. |
| Temporal score | Future timestamp check and an explicit `burst_ingested` fixture flag; no history-derived burst calculation. |
| Provenance score | Fixed mapping of provenance labels; not identity or signature verification. |
| Source credibility | Fixed mapping based on provenance strings. |

The engine computes the weighted score documented below and returns `ALLOW`, `FLAG`, `QUARANTINE`, or `BLOCK`. It does not currently pass decisions into the persistent SQLite quarantine/audit store. The store is a separately tested Sprint 1 primitive, not an integrated defense control.

## Score and thresholds

```text
trust(m) = 0.35 × semantic(m)
         + 0.15 × temporal(m)
         + 0.30 × provenance(m)
         + 0.20 × credibility(m)
```

| Decision | Score range | Current behavior |
|---|---:|---|
| `ALLOW` | score ≥ 0.75 | Marks the record as passed. |
| `FLAG` | 0.50 ≤ score < 0.75 | Marks it as passed with an annotation. |
| `QUARANTINE` | 0.30 ≤ score < 0.50 | Marks it as not passed; persistent store not wired to the engine. |
| `BLOCK` | score < 0.30 | Marks it as not passed; no alert path. |

SQLite write provenance records source, session, agent, timestamp, and content hash when callers attach a ledger to a backend. These fields are useful for local audit; they do not establish cryptographic identity or authentic lineage.

No model behavior, detector efficacy, threshold calibration, false-positive estimate, or defense latency overhead has been measured. See the [claims audit](claims-audit.md).
