# SentinelMem Architecture & System Design

SentinelMem is a cross-backend retrieval-time defense framework designed to protect Large Language Model (LLM) agents against memory poisoning attacks.

```
                           LLM Agent Query & Ingestion
                                       │
                                       ▼
                   ┌───────────────────────────────────────┐
                   │          Memory Backend Store         │
                   │   [ FAISS  •  Mem0  •  LangMem ]      │
                   └───────────────────┬───────────────────┘
                                       │  Candidate Retrieval (Top-k)
                                       ▼
    ┌──────────────────────────────────────────────────────────────────────┐
    │                🛡️ SentinelMem Trust & Defense Engine                 │
    │                                                                      │
    │  ┌───────────────────────┐              ┌─────────────────────────┐  │
    │  │     Semantic Drift    │              │    Temporal Anomaly     │  │
    │  │ Divergence & Distance │              │ Burst & Rate Detection  │  │
    │  └───────────┬───────────┘              └────────────┬────────────┘  │
    │              │                                       │               │
    │  ┌───────────┴───────────┐              ┌────────────┴────────────┐  │
    │  │  Provenance Integrity │              │   Source Credibility    │  │
    │  │ Lineage & Ingress Id  │              │ Weight & Verification   │  │
    │  └───────────┬───────────┘              └────────────┬────────────┘  │
    │              └───────────────────┬───────────────────┘               │
    │                                  ▼                                   │
    │                 Weighted Trust Score Fusion                          │
    │               TrustScore = ∑ (w_i · S_i) ∈ [0, 1]                    │
    │                                  │                                   │
    │                                  ▼                                   │
    │                     Policy Enforcement Layer                         │
    │              [ ALLOW | FLAG | QUARANTINE | BLOCK ]                   │
    └──────────────────────────────────┬───────────────────────────────────┘
                                       │  Sanitized Context Only
                                       ▼
                              LLM Agent Context
```

---

## 1. Core Subsystems

### 1.1 Memory Backend Adapters (`sentinelmem.backends`)
Provides a unified abstraction layer over heterogeneous memory stores:
- **`BaseMemoryBackend`**: Standard interface for ingestion, indexing, and vector similarity retrieval.
- **`FAISSBackend`**: Local high-performance dense vector index (`IndexFlatIP`, `IndexFlatL2`).
- **`Mem0Backend`**: Adapter for Mem0 multi-layered memory structures.
- **`LangMemBackend`**: Adapter for LangGraph/LangChain LangMem memory managers.

### 1.2 Attack Simulation Harness (`sentinelmem.attacks`)
Implements reproducible memory poisoning vectors:
- **`MINJAAttack`**: Memory Injection via Natural Jailbreak (query-only memory injection without direct database write permissions).
- **`SleeperAttack`**: Delayed-activation memory poisoning designed to lie dormant until triggered by specific query keywords or context states.
- **`DirectWriteAttack`**: Direct memory payload manipulation for evaluating unconstrained adversarial write models.

### 1.3 Multi-Signal Trust Defense Layer (`sentinelmem.defense`)
Analyzes retrieved candidate records before they are injected into the agent's prompt context:
1. **Semantic Drift ($S_{\text{drift}}$):** Evaluates embedding distance and contextual divergence between candidate records and trusted agent profile history.
2. **Temporal Anomaly ($S_{\text{temp}}$):** Detects sudden ingestion bursts and out-of-band write timestamps.
3. **Provenance Integrity ($S_{\text{prov}}$):** Verifies the origin chain, session ID, and cryptographic ingress signatures.
4. **Source Credibility ($S_{\text{cred}}$):** Computes weight based on verified actor role (system, user, external tool, untrusted web fetch).

### 1.4 Policy Enforcement Engine (`sentinelmem.defense.engine`)
Fuses individual trust signals into a composite score:
$$\text{TrustScore} = w_{\text{drift}} S_{\text{drift}} + w_{\text{temp}} S_{\text{temp}} + w_{\text{prov}} S_{\text{prov}} + w_{\text{cred}} S_{\text{cred}}$$

- **$\text{TrustScore} \ge \theta_{\text{allow}}$:** `ALLOW` $\rightarrow$ Memory injected into prompt.
- **$\theta_{\text{flag}} \le \text{TrustScore} < \theta_{\text{allow}}$:** `FLAG` $\rightarrow$ Memory injected with security disclaimer and reduced weight.
- **$\theta_{\text{block}} \le \text{TrustScore} < \theta_{\text{flag}}$:** `QUARANTINE` $\rightarrow$ Memory isolated into quarantine store for human/agent review.
- **$\text{TrustScore} < \theta_{\text{block}}$:** `BLOCK` $\rightarrow$ Memory dropped immediately from context.

### 1.5 Benchmark & Evaluation Suite (`sentinelmem.evaluation`)
Measures security and performance metrics:
- **Attack Success Rate (ASR):** Percentage of poisoned memories successfully injected into prompt context.
- **Defense Efficacy ($\Delta\text{ASR}$):** Reduction in ASR under SentinelMem policy enforcement.
- **Benign Utility Preservation (FPR):** Percentage of legitimate memories incorrectly flagged or blocked.
- **Latency Overhead:** Milliseconds spent during retrieval-time inspection.
