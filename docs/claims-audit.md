# Claim audit: current evidence boundary

This audit compares public claims with the checked-in implementation and result artifacts.

| Claim area | Repository evidence | Safe characterization |
|---|---|---|
| FAISS retrieval | `results/faiss_sentence_transformer.json` records a schema-v2 run with a pinned sentence-transformer model over the fixed synthetic corpus. `results/faiss_baseline.json` retains the prior hash-stub run. | Real sentence embeddings are used for synthetic retrieval plumbing; neither artifact measures agent attack success or defense efficacy. |
| Reproducibility | The new artifact records config/hash, seed, versions, source revision, per-query cases, metrics, and separate timing. Same-seed deterministic fields are covered by tests. | Reproducibility metadata and a deterministic fixture path exist. Clean-clone/manual checks still need owner verification. |
| Mem0/LangMem | `emulated_mem0_backend.py` and `emulated_langmem_backend.py` use local Python containers and NumPy. | Explicit emulations only; no upstream client integration. |
| Attacks | `run_experiment` inserts generated payload records with backend writes. No agent loop or extractor is present. | MINJA, sleeper, and direct-write remain labeled fixture generators, not reproductions. |
| Defense | The trust engine applies fixed heuristic scores. SQLite can persist write provenance, audit events, and quarantine rows, but the engine does not yet enforce through this storage layer. | Prototype detection decisions plus storage primitives; no integrated persistent mitigation/review workflow or validated effectiveness. |
| Dashboard | The ReUI console imports a stored result artifact. The standalone browser demo is separate and illustrative. | The console visualizes a local recorded run; it is not a live experiment service. |

## Artifact facts

The schema-v1 hash artifact is retained as historical evidence. The schema-v2 real-embedding artifact contains per-query records and metric values produced from the configured model revision and synthetic scenario. Timing is a separate, environment-specific observation. See the JSON files under `results/` for exact values; do not copy values into prose without checking the artifact.

The model identity is pinned to the immutable revision in `configs/faiss_baseline.json`; model usage follows the [Sentence Transformers documentation](https://sbert.net/docs/sentence_transformer/usage/usage.html).

## Terms to reserve

Do not claim attack success, real Mem0/LangMem compatibility, cross-backend defense, utility preservation, cryptographic provenance, production quarantine, or latency overhead until those outcomes are directly implemented, measured, and represented by reproducible artifacts.
