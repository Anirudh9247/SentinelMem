# SentinelMem Defense Model & Multi-Signal Trust Fusion

This document details the multi-signal trust scoring mechanism and retrieval-time policy enforcement engine.

---

## 1. Multi-Signal Trust Architecture

SentinelMem inspects candidate memory records at retrieval time before they are forwarded into the agent's context window. Each memory is evaluated across four orthogonal security signals:

### 1.1 Semantic Drift Score ($S_{\text{drift}} \in [0, 1]$)
* **Goal:** Detect sudden thematic shifts or incongruous instruction patterns.
* **Computation:**
  $$S_{\text{drift}} = 1.0 - \text{CosineDistance}(\mathbf{e}_{\text{memory}}, \mathbf{e}_{\text{trusted\_centroid}})$$
  Where $\mathbf{e}_{\text{trusted\_centroid}}$ represents the historical centroid of validated memories. Higher scores indicate alignment with established trust baseline.

### 1.2 Temporal Anomaly Score ($S_{\text{temp}} \in [0, 1]$)
* **Goal:** Detect suspicious ingestion burst patterns or temporal clustering typical of automated poisoning campaigns.
* **Computation:**
  $$S_{\text{temp}} = \exp\left(-\lambda \cdot \max(0, \text{Rate}_{\Delta t} - \mu_{\text{normal}})\right)$$
  Where $\text{Rate}_{\Delta t}$ is the number of memory writes in window $\Delta t$.

### 1.3 Provenance Integrity Score ($S_{\text{prov}} \in [0, 1]$)
* **Goal:** Validate the cryptographic or session-bound lineage of the memory record.
* **Categories:**
  - `trusted_system` / `verified_user`: $1.0$
  - `authenticated_tool`: $0.85$
  - `external_integration`: $0.50$
  - `untrusted_import` / `anonymous`: $0.10$

### 1.4 Source Credibility Score ($S_{\text{cred}} \in [0, 1]$)
* **Goal:** Weight the historical reliability and domain trust score of the producing subsystem.

---

## 2. Weighted Trust Fusion

The composite trust score $\mathcal{T}(m)$ for memory record $m$ is computed as:
$$\mathcal{T}(m) = w_1 S_{\text{drift}}(m) + w_2 S_{\text{temp}}(m) + w_3 S_{\text{prov}}(m) + w_4 S_{\text{cred}}(m)$$
$$\text{subject to } \sum_{i=1}^4 w_i = 1.0, \quad w_i \ge 0$$

*Default Configuration:* $w_{\text{drift}} = 0.30$, $w_{\text{temp}} = 0.20$, $w_{\text{prov}} = 0.30$, $w_{\text{cred}} = 0.20$.

---

## 3. Retrieval-Time Policy Enforcement

| Decision | Threshold Condition | Action Taken on Retrieved Memory |
|---|---|---|
| 🟢 **`ALLOW`** | $\mathcal{T}(m) \ge 0.75$ | Memory record passed cleanly to LLM prompt. |
| 🟡 **`FLAG`** | $0.50 \le \mathcal{T}(m) < 0.75$ | Memory injected with `[UNVERIFIED_CONTEXT]` security annotation. |
| 🟠 **`QUARANTINE`** | $0.30 \le \mathcal{T}(m) < 0.50$ | Memory isolated; omitted from prompt; logged for review. |
| 🔴 **`BLOCK`** | $\mathcal{T}(m) < 0.30$ | Memory dropped immediately; security alert dispatched. |
