# Evaluation definitions and current evidence

This document distinguishes synthetic retrieval metrics from research outcomes. The current system has no agent model or real backend integrations for Mem0/LangMem.

## Current artifacts

- `results/faiss_baseline.json`: retained schema-v1 hash-embedding plumbing run.
- `results/faiss_sentence_transformer.json`: schema-v2 real sentence-embedding run over the fixed synthetic corpus.
- `results/faiss_hash_fixture_v2.json`: schema-v2 hash-stub comparison run.
- `results/faiss_sentence_transformer_repeat.json`: repeated real-model run with the same config.
- `results/faiss_sentence_transformer_alt_seed.json`: historical fixed-scenario run; its seed changes metadata only.
- `results/faiss_seeded_query_matrix.json`: 20-seed schema-v2.1 matrix over a seeded, stratified query-paraphrase sample.

Read exact counts, scores, model revision, package versions, and timings from these JSON files. The real model does not make the corpus or outcomes real-world; this remains a small synthetic retrieval baseline without a defense comparison.

Schema-v2.1 records the sampling protocol and the exact selected query text in each case. The fixed v1 scenario remains the control and continues to produce the same query set for every seed. The opt-in stratified_query_variant_v1 protocol selects one paraphrase from each of four intent families using a stable SHA-256 ranking, so a seed chooses a reproducible query set without changing the corpus or global random state.

The current 20-seed matrix contains 80 query samples and observes all 16 authored variants. Its pooled unsafe-labelled retrieval rate is 23/80 (0.2875); per-seed rates range from 0 to 0.5, with mean 0.2875 and population standard deviation 0.163459. These are descriptive measurements from a small finite synthetic paraphrase pool. The matrix intentionally reports no confidence interval and is not an attack-success or defense-efficacy result.

## Prototype simulation counters

`run_experiment` still inserts attack-labelled fixture records directly, retrieves fixture queries, and applies the rule-based engine. Its ASR-named values remain proxies:

- **Unfiltered unsafe-query proportion:** fraction of fixture queries retrieving at least one record with the designated label.
- **Post-filter unsafe-query proportion:** fraction with such a record passed by the engine.
- **Difference:** subtraction of those proportions.
- **Benign rejection proportion:** retrieved benign records marked not passed divided by retrieved benign records. `FLAG` counts as passed.
- **Elapsed time:** query loop including local backend retrieval and scoring, not a paired defended-versus-raw overhead estimate.

## Research metrics still needed

Define attack outcome at the point a poisoned memory changes an agent response or action; do not equate retrieval with successful execution. Measure benign task utility separately from memory-level false positives. Use paired raw/defended protocols, repeated runs, confidence intervals, signal ablations, held-out evaluation, and latency distributions after freezing thresholds. These remain planned work and are tracked in [docs/carry-over.md](carry-over.md).
