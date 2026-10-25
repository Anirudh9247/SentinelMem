# Sprint carry-over register

No work is removed from the five-sprint plan. Items not completed in Sprint 1 remain on the upcoming sprint backlog.

## Sprint 1 verification carry-over

- Owner must execute every unchecked item in `docs/manual-checks.md` on a clean clone and attach the listed evidence. Automated tests do not replace these reviews.
- The fixed control remains intentionally seed-invariant. An opt-in seeded query-paraphrase sampler and 20-seed matrix are implemented. Expand and validate the finite query pool before making inferential claims.
- Repeat the real sentence-transformer baseline on the owner’s target research machine and compare deterministic metrics; runtime timing is expected to vary by environment.

## Planned work remains in scope

### Sprint 2 — Real backends and attack reproduction

- Implement Mem0 OSS and LangMem/LangGraph adapters and run the same backend contract tests against them.
- Rework direct-write, MINJA, and sleeper scenarios through local agent behavior with explicit success oracles; document deviations from cited setups.
- Produce the undefended attack-by-backend baseline matrix with repeated seeds and confidence intervals.

### Sprint 3 — Defense layer

- Connect the signal weights and policy to a backend-independent retrieval enforcement wrapper.
- Add quarantine review/release behavior, hash-chain tamper evidence, and optional LLM consistency checks with a no-LLM path.
- Measure defended versus undefended utility and latency, then complete the required owner review of quarantined and allowed examples.

### Sprint 4 — Multi-agent orchestration

- Add shared/handoff memory agent runs, cross-agent poisoning cases, resumable parallel matrix orchestration, and an adaptive attacker.

### Sprint 5 — Evaluation freeze and paper packaging

- Complete signal ablations, threshold/weight sensitivity, confidence intervals, error analysis, validity discussion, reproduction guide, and paper tables/figures.
- Audit every final public claim and paper citation against stored artifacts and approved venues.
