# SentinelMem Threat Model v0.1

## Purpose

This document defines the first evaluable scope for SentinelMem: retrieval-time
protection against untrusted memories that are returned for otherwise benign user
queries. It is deliberately narrow so results can be reproduced before the
project expands to multiple backends and defense signals.

## System under evaluation

The system has four components:

1. A memory ingestion path that assigns provenance to each record.
2. A vector retrieval backend that returns the top-*k* memories for a query.
3. A retrieval-time policy layer, introduced after the baseline.
4. A reporting layer that saves configuration and metrics with each result.

The initial baseline exercises only component 2. It uses a deterministic,
synthetic corpus and does not call an LLM or external service.

## Assets to protect

- Integrity of retrieved memory context.
- Correctness of the retrieval-time policy decision.
- Reproducibility of benchmark inputs, configuration, and outputs.
- Availability of retrieval within the documented latency budget.

## Adversary model

For the first benchmark, the adversary may introduce records through an
untrusted import path. Those records are labelled `instruction_shaped` and carry
untrusted provenance. The adversary cannot modify the benchmark runner,
configuration file, trusted records, result files, or the retrieval backend.

The current synthetic scenario intentionally contains neutral placeholders only.
It validates benchmark plumbing; it is not a reproduction of a production attack
or a claim about vulnerability of a real backend.

## Security objective and metric

An unsafe retrieval occurs when any top-*k* retrieved record has the unsafe
label associated with a benign query. The baseline reports:

- unsafe retrieval rate;
- per-query retrieved identifiers, labels, and similarity scores;
- retrieval latency; and
- SHA-256 of the exact configuration file.

The future defense acceptance criterion is set only after the baseline has been
run and reviewed. It must include both reduction in unsafe retrieval and a
false-positive/benign-utility measure.

## Out of scope for v0.1

- LLM prompt execution and model alignment claims.
- Direct-write access to production memory systems.
- Evaluation against real user memory or personal data.
- Cross-backend comparisons and claims of generality.
- Adaptive adversaries that observe defense scores or thresholds.

## Required changes before broader evaluation

Before adding Mem0 or LangMem, document each backend version, ingestion API,
metadata preservation behavior, embedding model, hardware, and the exact
authorized attack-evaluation protocol.
