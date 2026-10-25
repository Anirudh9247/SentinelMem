# FAISS synthetic retrieval artifact contract v2.1

## Goal

Record deterministic retrieval-plumbing runs over a fixed synthetic control or an opt-in seeded query-variant sample, using an explicitly configured embedding provider. Neither protocol is a security-efficacy experiment.

## Inputs

- Real-embedding config: `configs/faiss_baseline.json`.
- Hash fixture config: `configs/faiss_hash_fixture.json`.
- Seeded query-matrix config: `configs/faiss_seeded_sampling.json`.
- Records and queries: `src/sentinelmem/synthetic.py`.
- Backend: `FAISSBackend` with `IndexFlatIP` and normalized vectors.
- Default experiment embedder: pinned Sentence Transformers model and immutable revision from config. The deterministic hash embedder remains available as a test fixture.
- Fixed control: seed is metadata only; corpus and four canonical queries do not change.
- Seeded protocol: stratified_query_variant_v1 selects one query paraphrase from each of four fixed intent families using a stable SHA-256 ranking. The corpus remains fixed.

## Procedure

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,research]"
python -m sentinelmem.baseline --config configs/faiss_baseline.json --output results/faiss_sentence_transformer.json
```

The first run downloads the pinned model if it is not cached. Attack fixtures and inference run locally against synthetic text; this command does not call an LLM, Mem0, or LangMem.

Seeded matrix command: python scripts/run_seed_matrix.py --config configs/faiss_seeded_sampling.json --seed-start 20260822 --repeats 20 --output results/faiss_seeded_query_matrix.json

The matrix retains each seed's selected query text, retrieval cases, metrics, and timing, then reports descriptive per-seed and pooled rates. It does not claim inferential confidence intervals.

## Artifact schema

Schema `2.1` stores the complete parsed config and SHA-256 of the effective config, seed, source commit and dirty-state flag, Python and dependency versions, embedding identity/dimension, corpus counts, sampling protocol and selected query text, deterministic metrics, environment timing in a separate `timings` object, and per-query retrieved IDs, labels, scores, and unsafe-label flags. JSON uses sorted keys and an atomic replace.

Deterministic metrics and query cases should match on repeated runs with the same config/model/runtime. Timings are not deterministic. A dirty source tree is recorded as such; the commit field identifies `HEAD` and is not a claim that uncommitted edits are captured by that commit.

## Reproducibility notes

- Preserve configs and result JSON under version control for reported runs.
- Record runtime versions and model revision; do not silently update either between compared runs.
- Keep the fixed scenario as a stable control. Use the opt-in seeded query-variant protocol when estimating sensitivity to wording; do not describe retrieval variation as agent attack success or defense efficacy.
- The 16-variant pool is small and hand-authored. Treat its seed matrix as a protocol smoke test; expand and validate the query suite before inferential claims.
- Preserve host/dependency details for performance claims; one timing is environment-specific and not defense overhead.
- Existing schema-v1 and v2.0 artifacts remain valid historical outputs and are not overwritten by seeded runs.
