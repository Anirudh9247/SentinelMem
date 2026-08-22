# SentinelMem: Detailed Sprint Execution Plan (Sprints 1–8)

This document contains the granular execution plans, task checklists, and completion criteria for all eight two-week sprints.

---

## 🏃 Sprint 1: Lit Review & Guide Approval
- **Timeline:** Week 1–2 (Aug 22 – Sep 4)
- **Phase:** Phase 1 (Foundation)
- **Objective:** Complete 10-paper reference set, obtain guide sign-off, and finalize all literature citations.

### Tasks:
- [x] Verify all 10 papers exist & match characterizations (web search / Google Scholar).
- [x] Compile final BibTeX entries & verified citations.
- [ ] Submit literature review to guide for sign-off.
- [x] Lock paper title & abstract language.

### Completion Criteria:
- Guide-signed reference sheet.
- No arXiv preprints in the final paper set; all citations from peer-reviewed venues (ACM CCS, IEEE S&P, USENIX Security, NDSS, NeurIPS, ICML, ACL).

---

## 🏃 Sprint 2: Threat Model & Environment Setup
- **Timeline:** Week 2–3 (Sep 4 – Sep 18)
- **Phase:** Phase 1 (Foundation)
- **Objective:** Finalize threat model, establish development environment, and plan attack harnesses.

### Tasks:
- [ ] Write formal threat model document (attacker capabilities, assumptions, attack surface).
- [ ] Set up Mem0, LangMem, FAISS environments on dev machine.
- [ ] Design attack harness architecture (modular for 3 backends).
- [ ] Create test datasets & injection points.

### Completion Criteria:
- Threat model signed off by advisor.
- All 3 backends running locally with automated health check tests.
- Harness skeleton code and initial test suite committed.

---

## 🏃 Sprint 3: MINJA Attack Implementation
- **Timeline:** Week 4–5 (Sep 18 – Oct 2)
- **Phase:** Phase 2 (Attack Reproduction)
- **Objective:** Reproduce MINJA (query-only injection) attacks; achieve documented baseline success rates.

### Tasks:
- [ ] Implement MINJA query-generation module (semantic-aware injections).
- [ ] Run attack on Mem0 backend (target: 98%+ injection success).
- [ ] Run attack on LangMem backend.
- [ ] Run attack on FAISS backend.
- [ ] Document baseline metrics & attack traces.

### Completion Criteria:
- MINJA working across all 3 backends.
- Baseline success rates logged with reproducible test scripts.
- Attack trace logs saved in standard JSON format.

---

## 🏃 Sprint 4: Sleeper + Direct-Write Attacks
- **Timeline:** Week 6–7 (Oct 2 – Oct 16)
- **Phase:** Phase 2 (Attack Reproduction)
- **Objective:** Implement sleeper/delayed-trigger and direct-write attacks; establish comparative baseline.

### Tasks:
- [ ] Implement sleeper-poisoning attack (dormant trigger, time/session-based activation).
- [ ] Implement direct-write attack (for backends supporting direct insertion).
- [ ] Test on all 3 backends, document success rates.
- [ ] Create comparative attack-success table (MINJA vs. sleeper vs. direct-write).

### Completion Criteria:
- All 3 attack types operational.
- Cross-backend comparison matrix published.
- Attack vectors documented with sample payloads.

---

## 🏃 Sprint 5: Trust-Signal Layer Design & Implementation
- **Timeline:** Week 8–9 (Oct 16 – Oct 30)
- **Phase:** Phase 3 (Defense Core)
- **Objective:** Design & code multi-signal trust fusion; integrate retrieval-time policy checks.

### Tasks:
- [ ] Define trust signals: semantic drift, temporal anomaly, provenance, source credibility.
- [ ] Build signal-extraction modules (backend-agnostic).
- [ ] Implement weighted fusion & scoring algorithm.
- [ ] Create retrieval-time policy enforcement (block, quarantine, flag).
- [ ] Validate on all 3 backends with test cases.

### Completion Criteria:
- Trust-scoring library complete and unit tested.
- Retrieval-time policy enforcement verified across backends without backend-specific hacks.

---

## 🏃 Sprint 6: Dashboard Prototype & Evaluation Framework
- **Timeline:** Week 10–11 (Oct 30 – Nov 13)
- **Phase:** Phase 3 (Defense Core)
- **Objective:** Build React security dashboard; finalize benchmarking & evaluation harness.

### Tasks:
- [ ] Design dashboard wireframe (trust signals, policy decisions, attack logs).
- [ ] Implement React components (signal visualization, heatmaps, trace replay).
- [ ] Build full evaluation harness (attack × defense × metric combinations).
- [ ] Draft paper outline & figures (attack success vs. defense success).

### Completion Criteria:
- Dashboard prototype functional and capable of replaying attack traces.
- Evaluation harness fully automated for batch runs.
- Benchmark data collection pipeline validated.

---

## 🏃 Sprint 7: Full Benchmarking & Paper Writeup
- **Timeline:** Week 12–14 (Nov 13 – Nov 27)
- **Phase:** Phase 4 (Benchmarking & Paper)
- **Objective:** Run full benchmark suite, write & refine research paper, prepare for submission.

### Tasks:
- [ ] Run full benchmarking: attack success, defense efficacy, false-positive rate, latency.
- [ ] Analyze results, identify edge cases & failure modes.
- [ ] Write paper sections: intro, related work, methodology, results, discussion.
- [ ] Create final figures & tables for paper.
- [ ] Submit to guide for review & feedback.

### Completion Criteria:
- Full paper draft (6000+ words).
- All benchmark metrics reproducible with one command.
- Advisor feedback received and cataloged for revision.

---

## 🏃 Sprint 8: Open-Source Release & Presentation
- **Timeline:** Week 15–16 (Nov 27 – Dec 11)
- **Phase:** Phase 4 (Final Delivery)
- **Objective:** Package SentinelMem as open-source repo, finalize presentation, submit paper.

### Tasks:
- [ ] Clean up codebase, add documentation & README.
- [ ] Publish GitHub repo (public or org-private per advisor preference).
- [ ] Create presentation slides (methodology, results, impact).
- [ ] Finalize & submit research paper (with full guide approval).
- [ ] Prepare for final presentation or defense.

### Completion Criteria:
- Clean, documented GitHub repository.
- Final research paper submitted.
- Slide deck completed and rehearsed.
- All semester deliverables archived.
