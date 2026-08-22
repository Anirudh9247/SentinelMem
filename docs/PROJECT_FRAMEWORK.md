# SentinelMem: 14–16 Week Project Management Framework

**Project Title:** *SentinelMem: Cross-Backend Defense Against Memory Poisoning in LLM Agents*  
**Timeline:** August 22 – December 11 (16 Weeks)  
**Author / Team:** Research Student / Core Development Team  

---

## 1. Executive Summary & Framework Architecture

The **SentinelMem** Project Management Framework is engineered specifically for a rigorous academic semester research lifecycle. It bridges foundational literature validation, multi-backend attack reproduction (MINJA, sleeper poisoning, direct write), multi-signal trust defense implementation, comprehensive benchmarking, and peer-reviewed paper submission.

### The Five Operational Tools:
1. **Overview**: Project snapshot, phase milestones, and real-time status indicators.
2. **Sprint Plan**: 8 two-week sprints with strict objective definitions and sign-off criteria.
3. **Checklists**: 3 layers (Retrospective, Implementation Execution, and Research & Writing) with hourly budgets.
4. **Weekly Tracking**: Friday EOD status updates, variance analysis ($\pm 15\%$ triggers), and escalation logs.
5. **Dependencies & Risks**: Critical path mapping, built-in buffers (W11 & W14), 9 prioritized risks, and scope reduction triggers.

---

## 2. Semester Timeline & Phase Breakdown

```
Phase 1: Foundation & Threat Modeling     [Weeks 1–3  | Aug 22 – Sep 18]
Phase 2: Attack Reproduction & Baselines  [Weeks 4–7  | Sep 18 – Oct 16]
Phase 3: Defense Design & Signal Fusion   [Weeks 8–11 | Oct 16 – Nov 13]
Phase 4: Full Benchmarking & Paper        [Weeks 12–16| Nov 13 – Dec 11]
```

### Phase 1: Foundation & Threat Modeling (Weeks 1–3)
- Finalize and sign off on 10 peer-reviewed reference papers (no arXiv papers in final reference set).
- Formalize threat model document: adversary capability (black-box vs. gray-box), injection mechanisms, and victim agent memory surface.
- Set up local test environments for Mem0, LangMem, and FAISS.

### Phase 2: Attack Reproduction & Baselines (Weeks 4–7)
- Reproduce MINJA (query-only injection) attack to establish documented baseline success rates ($98.2\%$ injection rate on vulnerable backends).
- Implement sleeper/delayed-trigger and direct-write attacks.
- Standardize multi-backend attack traces and reproducible experiment logs.

### Phase 3: Defense Design & Signal Fusion (Weeks 8–11)
- Develop multi-signal trust scoring library:
  - **Semantic Drift:** Cosine distance and embedding clustering variance.
  - **Temporal Anomaly:** Injection burst patterns and retrieval cadence.
  - **Provenance Tracking:** Ingress origin, session lineage, and interaction context.
  - **Source Credibility:** Verified identity scoring and external tool assertions.
- Implement retrieval-time policy enforcement engine (Block, Quarantine, Flag).
- Build security dashboard prototype for threat visualization.

### Phase 4: Full Benchmarking & Paper Writeup (Weeks 12–16)
- Execute complete benchmark across 3 backends $\times$ 3 attack vectors $\times$ defense configurations.
- Measure attack success reduction, defense precision/recall, false-positive rates, and retrieval latency overhead.
- Draft 6000+ word research paper and incorporate guide revisions.
- Open-source codebase release on GitHub with full reproducibility documentation.

---

## 3. Weekly & Monthly Governance Cadence

### Weekly Rhythm (Every Friday EOD)
1. Complete the standard Weekly Status Update template.
2. Measure planned vs. actual hours worked and calculate variance ($\Delta\%$).
3. If variance exceeds $\pm 15\%$ or a task slipped by $>3$ days, review critical path impact.
4. Flag any red-flag escalation triggers immediately.

### Monthly Guide Check-ins (30 Minutes)
- **Check-in 1 (Week 5 | Sep 25):** Review reproduced MINJA baseline results and threat model document.
- **Check-in 2 (Week 9 | Oct 23):** Review trust-signal fusion architecture and preliminary defense benchmarks.
- **Check-in 3 (Week 13 | Nov 20):** Review full paper draft, benchmark figures, and discussion section.

---

## 4. Key Performance Indicators (KPIs)

- **Attack Reproduction:** Reproduce MINJA with $\ge 95\%$ baseline success on unmitigated backends.
- **Defense Efficacy:** Reduce attack success rate below $5\%$ while maintaining false-positive rate $<3\%$.
- **Latency Overhead:** Keep defense retrieval-time trust computation under $45\text{ ms}$.
- **Paper Quality:** Full 6000+ word draft adhering to standard IEEE/ACM formatting guidelines with 10+ peer-reviewed citations.
