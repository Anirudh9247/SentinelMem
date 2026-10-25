# SentinelMem prototype and reproducibility scaffold

SentinelMem explores retrieval-time trust scoring on synthetic memory records. It is a research prototype, not a validated defense for live LLM agents.

## Implemented

- A fixed synthetic corpus and a deterministic hash embedding kept as a test fixture.
- A common backend contract and a FAISS `IndexFlatIP` adapter that can use real, pinned sentence embeddings.
- A versioned run artifact with the full config and hash, seed, runtime package versions, source commit/dirty state, per-query retrievals, metrics, and separate environment timing.
- An opt-in deterministic seed matrix that samples query paraphrases across intent families, records selected text per run, and summarizes synthetic retrieval variation without changing the fixed control.
- SQLite persistence primitives for write-time source/session/agent/content-hash provenance, audit events, and quarantine records.
- A rule-based retrieval-filtering simulation. Its outcome counters are fixture proxies, not agent security metrics.
- A ReUI console that reads a stored result artifact from `results/`. It does not connect to an API or live memory service.
- Explicitly named local `EmulatedMem0Backend` and `EmulatedLangMemBackend` classes. They do not import those upstream products.

The experiment still has no connected agent, conversation-memory extraction, real Mem0/LangMem integration, calibrated defense, or measured cross-backend efficacy. The hash-vector artifact in `results/faiss_baseline.json` is retained as historical plumbing evidence. The fixed baseline remains the control; a separate seeded query-variant matrix tests reproducible wording sensitivity without changing it. See [the claim audit](docs/claims-audit.md) and [the carry-over register](docs/carry-over.md).

## Install and run

Create an environment and install the research dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev,research]"
```

If `.venv` was copied from another machine or its Python installation was removed, recreate it before installing dependencies; virtual environments store the original Python path.

The first real-embedding run downloads the pinned model revision if it is not cached. Model inference and the attack fixtures run locally against synthetic data.

Run the real sentence-embedding FAISS baseline:

```powershell
python -m sentinelmem.baseline --config configs/faiss_baseline.json --output results/faiss_sentence_transformer.json
```

Run the seeded query-variant matrix separately from the fixed control:

    python scripts/run_seed_matrix.py --config configs/faiss_seeded_sampling.json --seed-start 20260822 --repeats 20 --output results/faiss_seeded_query_matrix.json

The matrix records each seed's sampled query text and per-seed outcomes. It reports descriptive synthetic retrieval variation only; the current finite query pool is too small for inferential confidence intervals.

Run the hash fixture separately:

```powershell
python -m sentinelmem.baseline --config configs/faiss_hash_fixture.json --output results/faiss_hash_fixture_v2.json
```

The real baseline uses `sentence-transformers/all-MiniLM-L6-v2` at the immutable revision recorded in the config. The model produces 384-dimensional sentence vectors; this is a real embedding model over a synthetic corpus, not an agent or defense evaluation. See the [model card](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2/tree/c21050a7ef692090620a6d037dd736908f9c7cf6) and [Sentence Transformers usage docs](https://sbert.net/docs/sentence_transformer/usage/usage.html).

Run the local fixture simulation:

```powershell
sentinelmem --backend faiss --attack minja --top-k 3
sentinelmem --backend emulated_mem0 --attack minja --top-k 3
sentinelmem --backend emulated_langmem --attack sleeper --top-k 3
```

The attack classes still insert labelled payloads directly. They do not reproduce MINJA or delayed triggers through an agent loop.

## Checks and UI

The frontend build requires Node.js 22.12 or newer and pnpm 9 or newer. Install its locked dependencies once before running the checks:

```powershell
pnpm --dir frontend install --frozen-lockfile
```

```powershell
make check
```

On Windows without `make`, run `.\scripts\check.ps1`. The check runs pytest, Ruff, and the React production build.

Run the research console with:

```powershell
cd frontend
pnpm install
pnpm dev
```

The console reads `results/faiss_sentence_transformer.json` as a local artifact. Cards and chart values describe that stored synthetic run. The standalone browser demo (`index.html` and `app.js`) remains a separate illustrative simulation.

For a local storage restart smoke check, run `python scripts/manual_storage_check.py`. Owner-run manual verification is listed in [docs/manual-checks.md](docs/manual-checks.md).

## Evidence and status

The schema-v1 file `results/faiss_baseline.json` preserves the earlier 64-dimensional deterministic-hash run and its recorded timing. Schema-v2.1 runs record the exact sampled query text and place deterministic metrics separately from environment-specific timings. Every generated result records its effective configuration and library versions. See [the experiment contract](docs/experiment-contract.md), [evaluation status](docs/evaluation.md), and [claims audit](docs/claims-audit.md).
