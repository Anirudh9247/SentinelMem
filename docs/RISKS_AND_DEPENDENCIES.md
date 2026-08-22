# SentinelMem: Critical Path, Dependencies & Risk Mitigation Register

This document defines the critical path forward, timeline buffers, risk mitigation catalog, and predefined scope reduction triggers.

---

## 🛑 1. Critical Path & Dependency Flow

Any slippage in the **Red Path** directly compresses paper writeup and submission review:

$$\text{Phase 1 (Foundation)} \longrightarrow \text{Phase 2 (Attacks)} \longrightarrow \text{Phase 3 (Defense)} \longrightarrow \text{Phase 4 (Paper)}$$

```
Phase 1 [W1–3]: Lit review signed & Threat model
       │
       ▼ (Unblocks Phase 2)
Phase 2 [W4–7]: MINJA, Sleeper & Direct-Write Baselines
       │
       ▼ (Blocks Phase 3 defense design decisions)
Phase 3 [W8–11]: Trust-Signal Fusion & Policy Enforcement
       │
       ▼ (Blocks Benchmarking & Paper metrics)
Phase 4 [W12–16]: Full Benchmark Suite & 6000+ Word Paper
       │
       ▼ (Blocks Final Submission & Defense)
Final Deliverables: Open-Source Release, Slide Deck & Submission
```

### Parallel Dependencies (Non-Critical Path)
- **Security Dashboard UI (Weeks 10–11):** Independent frontend prototype; if delayed, does not block core benchmark results or paper writing.
- **GitHub Packaging (Weeks 15–16):** Final open-source repository release; executed after the core paper is finalized.

---

## 🛡️ 2. Contingency Buffers

To prevent deadline cascade failures, the schedule incorporates two dedicated contingency buffers:

1. **Week 11 Buffer (3–4 Days):**
   - *Location:* End of Phase 3, immediately prior to Phase 4 benchmark kickoff.
   - *Purpose:* Absorb trust-signal integration overruns and ensure evaluation harness stability.

2. **Week 14 Buffer (2–3 Days):**
   - *Location:* Middle of Phase 4, prior to final advisor review.
   - *Purpose:* Re-run anomalous benchmark configurations and incorporate unexpected advisor revisions.

---

## ✂️ 3. Predefined Scope Reduction Triggers

If slippage occurs despite contingency buffers, execute these predefined scope reductions:

- **If Phase 2 slips $>1$ week:**
  - *Action:* Reduce attack variant count (focus strictly on sleeper/delayed poisoning and MINJA; defer direct-write comparison).
- **If Phase 3 slips $>1$ week:**
  - *Action:* Defer standalone React dashboard to post-submission; focus exclusively on core signal fusion algorithms and benchmark figures.
- **If Phase 4 timeline compresses:**
  - *Action:* Trim paper narrative to core results; move exhaustive parameter ablations and supplementary analyses to the appendix.

---

## ⚠️ 4. Master Risk Register & Mitigation Playbook

| # | Severity | Risk Description | Potential Impact | Concrete Mitigation Strategy |
|---|:---:|---|---|---|
| **R1** | 🔴 **High** | Attack reproduction slower than planned | Delays defense design by 1–2 weeks; compresses Phase 4 writeup. | Start attack harness skeleton in Week 2 in parallel with threat model; pre-stage test datasets; prepare synthetic attack harness fallback. |
| **R2** | 🔴 **High** | Trust-signal extraction complexity underestimated | Defense quality degrades or timeline slips past Week 10. | Prototype signal extraction in Week 7; prioritize top 2–3 signals (semantic drift & temporal anomaly) if full fusion cannot finish by Week 9. |
| **R3** | 🟠 **Medium** | Guide feedback on paper arrives late (Week 14+) | Final revisions compress into Week 15, risking submission quality. | Submit preliminary methodology & threat model by Week 12 end; request incremental feedback rather than monolithic review. |
| **R4** | 🟠 **Medium** | Benchmarking infrastructure crashes / timeouts | Benchmark results delayed; reproducibility damaged. | Build checkpointing and recovery in Week 9; run dry runs in Week 11; keep manual CSV result fallback. |
| **R5** | 🟠 **Medium** | Team member availability / unexpected absence | Critical path tasks blocked on single point of failure. | Cross-document all code and architectural decisions weekly; maintain clean docstrings and setup guides. |
| **R6** | 🟠 **Medium** | Upstream API breaking changes (Mem0 / LangMem) | Integration breaks during benchmark evaluation. | Pin exact package versions in lockfiles; create mock interface tests. |
| **R7** | 🟠 **Medium** | Direct-write attack not supported on all backends | Asymmetric comparison matrix in paper. | Create explicit abstraction separating direct-write memory backends from query-only backends. |
| **R8** | 🟢 **Low** | False-positive rate too high under trust scoring | Benign queries inappropriately blocked or flagged. | Implement tiered policy enforcement (Flag vs. Quarantine vs. Block) with adjustable sensitivity thresholds. |
| **R9** | 🟢 **Low** | Paper formatting / template mismatches at submission | Last-minute compilation panic before submission. | Use official IEEE/ACM LaTeX templates from Week 11; maintain continuous compilation on Overleaf or local TeX engine. |
