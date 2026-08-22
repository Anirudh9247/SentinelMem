# SentinelMem Experiment Contract v0.1

## Goal

Produce one deterministic FAISS retrieval baseline that any contributor can run
from a clean environment and inspect without network access after dependencies
are installed.

## Inputs

- Configuration: `configs/faiss_baseline.json`.
- Corpus and queries: fixed synthetic records in `src/sentinelmem/synthetic.py`.
- Backend: `faiss-cpu`, pinned through the project dependency range and later
  captured in a lockfile.
- Embedding: deterministic hash-based stub, explicitly not a semantic embedding
  model and not suitable for research conclusions.

## Procedure

1. Create a Python virtual environment.
2. Install the package and its development dependencies.
3. Run the baseline command below.
4. Run the automated tests.
5. Preserve the generated JSON outside Git or attach it to the experiment record.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m sentinelmem.baseline --config configs/faiss_baseline.json --output results/faiss_baseline.json
pytest
```

## Expected output contract

`results/faiss_baseline.json` must contain the benchmark/schema identifiers,
scenario, seed, embedding definition, corpus counts, metrics, per-query result,
and configuration SHA-256. Generated results are excluded from Git to prevent
accidental mixing of runs with source artifacts.

## Reproducibility rules

- Change configuration through a committed JSON file, never an undocumented
  command-line edit.
- Record the Python version, OS, `pip freeze`, Git commit, and output file hash
  with each reported result.
- Do not compare runs where corpus, query set, top-*k*, backend, or embedding
  definition differs without labelling the comparison as non-equivalent.
- Treat latency as environment-specific; report hardware and run at least five
  repetitions before drawing a conclusion.

## v0.1 acceptance criteria

- The command creates parseable JSON at the requested output path.
- The same inputs produce the same record labels and retrieval ordering.
- Unit tests pass from a clean environment.
- The scope and limitations in `docs/threat-model.md` are preserved in any
  presentation of the result.
