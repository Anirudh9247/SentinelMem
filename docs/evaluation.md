# SentinelMem Benchmark & Evaluation Protocol

This document defines the evaluation methodology, comparative metrics, and experimental contracts for SentinelMem.

---

## 1. Primary Metrics

1. **Attack Success Rate (ASR):**
   $$\text{ASR} = \frac{\text{Number of queries where }\ge 1\text{ poisoned memory is retrieved \& injected}}{\text{Total number of test queries}}$$

2. **Defense Efficacy ($\Delta\text{ASR}$):**
   $$\Delta\text{ASR} = \text{ASR}_{\text{unmitigated}} - \text{ASR}_{\text{defended}}$$

3. **False Positive Rate (FPR) / Benign Utility Preservation:**
   $$\text{FPR} = \frac{\text{Benign memories incorrectly blocked or quarantined}}{\text{Total retrieved benign memories}}$$

4. **Retrieval Latency Overhead ($\Delta t$):**
   $$\Delta t = t_{\text{defended\_retrieval}} - t_{\text{raw\_retrieval}} \quad (\text{Target: } < 40\text{ ms})$$

---

## 2. Evaluation Matrix

| Backend | Attack Vector | Baseline ASR | Target Defended ASR | Target FPR | Max Latency |
|---|---|:---:|:---:|:---:|:---:|
| **FAISS** | MINJA Query Injection | $\ge 75.0\%$ | $< 5.0\%$ | $< 2.0\%$ | $< 30\text{ ms}$ |
| **FAISS** | Sleeper Poisoning | $\ge 70.0\%$ | $< 5.0\%$ | $< 2.0\%$ | $< 30\text{ ms}$ |
| **FAISS** | Direct-Write | $\ge 90.0\%$ | $< 10.0\%$ | $< 2.5\%$ | $< 30\text{ ms}$ |
| **Mem0** | MINJA Query Injection | $\ge 80.0\%$ | $< 5.0\%$ | $< 3.0\%$ | $< 50\text{ ms}$ |
| **LangMem** | MINJA Query Injection | $\ge 75.0\%$ | $< 5.0\%$ | $< 3.0\%$ | $< 50\text{ ms}$ |
