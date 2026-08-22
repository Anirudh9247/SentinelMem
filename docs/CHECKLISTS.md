# SentinelMem: Three-Tier Project Checklists & Effort Budgets

This document outlines the three layers of deliverables with estimated effort in hours and hard deadlines.

---

## 🏛️ Layer 1: Retrospective Checklist (Work Completed to Date)

| Status | Deliverable | Summary & Verification |
|---|---|---|
| ✅ **Completed** | **Title Locked** | *SentinelMem: Cross-Backend Defense Against Memory Poisoning in LLM Agents* |
| ✅ **Completed** | **Literature Review** | 11 papers analyzed, comparative matrix + gap analysis compiled |
| ⏳ **Pending Approval** | **Reference Sheet** | 10 peer-reviewed papers with BibTeX, abstracts, and links ready for guide sign-off |
| ✅ **Completed** | **PowerPoint Deck** | Title, MINJA figures (98.2%, 76.8%), jargon fixes, OWASP citation finalized |
| ✅ **Completed** | **Word Report** | Three embedded tables (trust signals, defense comparison, lit gaps) production-ready |
| ✅ **Completed** | **Research Gap Identified** | Cross-backend retrieval-time memory trust governance not covered in prior work |

---

## 💻 Layer 2: Implementation Execution Checklist (112 Hours Total)

*Phase 2–3: Attack reproduction & defense core codebase modules.*

| Done | Module & Scope | Detailed Tasks | Est. Hours | Deadline |
|:---:|---|---|:---:|:---:|
| [ ] | **Attack Harness Module** | Query-generation, semantic injection strategies, success evaluation metric | **20 hrs** | Week 5 end |
| [ ] | **Mem0 Integration** | Initialize, poison, retrieve—test all 3 attack types on Mem0 backend | **12 hrs** | Week 6 end |
| [ ] | **LangMem Integration** | Adapt harness to LangMem memory abstraction and API | **10 hrs** | Week 7 end |
| [ ] | **FAISS Integration** | Custom vector database setup, memory extraction, attack adaptation | **14 hrs** | Week 7 end |
| [ ] | **Trust-Signal Library** | Semantic drift, temporal anomaly, provenance, credibility scoring | **30 hrs** | Week 9 end |
| [ ] | **Policy Enforcement Layer** | Retrieval-time blocking, quarantine logic, dynamic thresholding | **20 hrs** | Week 10 end |
| [ ] | **Multi-Backend Abstraction** | Backend-agnostic retrieval interface and plugin architecture | **16 hrs** | Week 10 end |

**Total Implementation Effort:** **112 Hours**

---

## 📝 Layer 3: Research & Writing Checklist (107 Hours Total)

*Literature, threat model, benchmarking framework, and paper deliverables.*

### Weeks 1–3: Literature & Threat Model
| Done | Deliverable | Description & Scope | Est. Hours | Deadline |
|:---:|---|---|:---:|:---:|
| [x] | **Verify All 10 Papers** | Check DOI, confirm venue, verify no preprints | **5 hrs** | Week 2 end |
| [ ] | **Formal Threat Model** | Attacker model, assumptions, attack surface definition | **8 hrs** | Week 3 end |
| [ ] | **Guide Sign-Off** | Submit literature review & reference sheet; incorporate feedback | **2 hrs** | Week 3 end |

### Weeks 4–11: Methodology & Results
| Done | Deliverable | Description & Scope | Est. Hours | Deadline |
|:---:|---|---|:---:|:---:|
| [ ] | **Benchmarking Design** | Metrics (attack success, defense success, false positives, latency) | **8 hrs** | Week 6 end |
| [ ] | **Attack $\times$ Defense Matrix** | Plan full experiment combinations | **4 hrs** | Week 8 end |
| [ ] | **Full Benchmarking Run** | Execute all experiments, log results across 3 backends | **40 hrs** | Week 14 mid |
| [ ] | **Results Analysis** | Interpret metrics, identify outliers and patterns | **16 hrs** | Week 14 end |

### Weeks 12–15: Paper Writeup & Finalization
| Done | Deliverable | Description & Scope | Est. Hours | Deadline |
|:---:|---|---|:---:|:---:|
| [ ] | **Paper Writeup** | Intro, related work, methodology, results, discussion (6000+ words) | **34 hrs** | Week 13 end |
| [ ] | **Guide Review & Final Submission** | Revise per advisor comments, format template, verify citations | **8 hrs** | Week 15 end |

**Total Research & Writing Effort:** **107 Hours**  
**Cumulative Project Effort:** **219 Hours**
