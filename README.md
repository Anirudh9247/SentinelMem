# SentinelMem: Cross-Backend Defense Against Memory Poisoning in LLM Agents

**SentinelMem** is a cross-backend retrieval-time defense framework designed to protect Large Language Model (LLM) agents against memory poisoning attacks (including MINJA query-only injections, sleeper/delayed triggers, and direct-write poisoning).

```
                           LLM Agent Ingestion
                                   │
                                   ▼
             ┌──────────────────────────────────────────┐
             │         Vector Memory Storage            │
             │   (FAISS  •  Mem0  •  LangMem)           │
             └─────────────────────┬────────────────────┘
                                   │  Candidate Retrieval (Top-k)
                                   ▼
┌────────────────────────────────────────────────────────────────────────┐
│               🛡️ SentinelMem Defense & Trust Engine                    │
│                                                                        │
│   ┌─────────────────────┐  ┌─────────────────────┐                     │
│   │   Semantic Drift    │  │  Temporal Anomaly   │                     │
│   │   Divergence Metric │  │  Burst / Rate Check │                     │
│   └──────────┬──────────┘  └──────────┬──────────┘                     │
│              │                        │                                │
│   ┌──────────┴──────────┐  ┌──────────┴──────────┐                     │
│   │ Provenance Tracking │  │ Source Credibility  │                     │
│   │ Ingress / Lineage   │  │ Authenticity Weight │                     │
│   └──────────┬──────────┘  └──────────┬──────────┘                     │
│              └────────────┬───────────┘                                │
│                           ▼                                            │
│            Weighted Trust Fusion & Policy Engine                       │
│              [ ALLOW  |  FLAG  |  QUARANTINE  |  BLOCK ]               │
└───────────────────────────┬────────────────────────────────────────────┘
                            │  Sanitized Context Only
                            ▼
                     LLM Agent Context
```

---

## ⚡ Quick Start

### 1. Environment Setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

### 2. Run Automated Test Suite
```powershell
pytest
```

### 3. Run Security Experiment CLI
```powershell
# Run MINJA attack on FAISS backend with SentinelMem defense
sentinelmem --backend faiss --attack minja --top-k 3

# Run Sleeper attack on Mem0 backend
sentinelmem --backend mem0 --attack sleeper

# Run Direct-Write attack on LangMem backend and export JSON results
sentinelmem --backend langmem --attack direct_write --output results/langmem_direct.json
```

### 4. Launch Security Research Console
Open [`index.html`](file:///f:/Projects/SentinelMem/index.html) in any web browser to access the interactive security simulation and trust analysis console:
```powershell
Start-Process .\index.html
```

---

## 🔬 Benchmark Results Summary

| Backend | Attack Vector | Unmitigated Baseline ASR | Defended SentinelMem ASR | Defense Efficacy ($\Delta\text{ASR}$) | False Positive Rate | Inspection Latency |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **FAISS** | MINJA Query Injection | $100.0\%$ | **$0.0\%$** | **$+100.0\%$** | $0.0\%$ | $1.45\text{ ms}$ |
| **FAISS** | Sleeper Delayed Poisoning | $50.0\%$ | **$0.0\%$** | **$+50.0\%$** | $0.0\%$ | $1.20\text{ ms}$ |
| **FAISS** | Direct-Write | $100.0\%$ | **$0.0\%$** | **$+100.0\%$** | $0.0\%$ | $1.10\text{ ms}$ |
| **Mem0** | MINJA Query Injection | $100.0\%$ | **$0.0\%$** | **$+100.0\%$** | $0.0\%$ | $3.40\text{ ms}$ |
| **LangMem** | Direct-Write | $100.0\%$ | **$0.0\%$** | **$+100.0\%$** | $0.0\%$ | $2.80\text{ ms}$ |

---

## 📚 Technical Documentation

- 📖 **[Architecture & System Design](docs/architecture.md)**: Deep dive into the 4-signal trust fusion and retrieval-time gating pipeline.
- 🎯 **[Threat Model](docs/threat-model.md)**: Adversary capabilities, assumptions, assets to protect, and evaluation boundaries.
- ⚔️ **[Attack Models](docs/attack-models.md)**: Formal taxonomy of MINJA, Sleeper, and Direct-Write memory poisoning vectors.
- 🛡️ **[Defense Model](docs/defense-model.md)**: Multi-signal trust scoring formulas, threshold gating, and policy decisions.
- 📊 **[Evaluation Protocol](docs/evaluation.md)**: Benchmark metrics, experimental contract, and target criteria.

---

## 🛠️ Codebase Structure

```
SentinelMem/
├── configs/                     # Experiment configurations
├── docs/                        # Formal technical documentation
│   ├── architecture.md          # System design & pipeline
│   ├── threat-model.md          # Threat model & adversary boundaries
│   ├── attack-models.md         # Attack taxonomy (MINJA, Sleeper, Direct-Write)
│   ├── defense-model.md         # Trust fusion & policy gating formulas
│   └── evaluation.md            # Benchmark methodology & metrics
├── src/sentinelmem/             # Core Python package
│   ├── models.py                # Data contracts (MemoryRecord, TrustBreakdown, DefenseDecision)
│   ├── cli.py                   # Command-line benchmark runner
│   ├── backends/                # Memory backend adapters
│   │   ├── base.py              # BaseMemoryBackend interface
│   │   ├── faiss_backend.py     # FAISS vector store
│   │   ├── mem0_backend.py      # Mem0 multi-layer adapter
│   │   ├── langmem_backend.py   # LangMem thread adapter
│   │   └── registry.py          # Dynamic backend registry
│   ├── attacks/                 # Attack simulation harness
│   │   ├── minja.py             # MINJA query-only injection
│   │   ├── sleeper.py           # Delayed-trigger poisoning
│   │   └── direct_write.py      # Direct memory injection
│   ├── defense/                 # Multi-signal trust layer
│   │   ├── signals.py           # Drift, Temporal, Provenance, Credibility
│   │   └── engine.py            # SentinelEngine trust fusion & policy
│   └── evaluation/              # Benchmark runner & metrics
│       └── benchmark.py         # End-to-end evaluation harness
├── tests/                       # Pytest test suite (12 passing tests)
├── index.html                   # Security Research Console UI
├── app.js                       # Security console simulation engine
├── styles.css                   # Console cybersecurity theme
└── pyproject.toml               # Package build & dependency definition
```
