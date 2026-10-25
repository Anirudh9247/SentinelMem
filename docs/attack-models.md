# Attack-labelled fixtures and their limits

The Python package includes three payload generators named after memory-poisoning scenarios. They provide labelled inputs for plumbing and policy demonstrations; they are not faithful reproductions of published attacks.

## MINJA-labelled fixture

`MINJAAttack` returns four instruction-shaped `MemoryRecord` objects and four related query strings. `run_experiment` inserts the records directly with `backend.add`. There is no adversarial conversation, LLM, automatic memory extraction, or query-only write path. The name indicates the motivating scenario, not a reproduced MINJA attack.

## Sleeper-labelled fixture

`SleeperAttack` returns two instruction-shaped records with trigger text in their content and older timestamps. No trigger state machine activates them, and the current temporal heuristic does not detect their age. This fixture does not evaluate delayed activation or sleeper behavior.

## Direct-write-labelled fixture

`DirectWriteAttack` returns two instruction-shaped records, which the harness inserts through the same local backend interface used for other payloads. It does not bypass or exploit an upstream service's access controls and does not establish an upper bound for an external attack.

## Evaluation boundary

The current harness measures whether a record with the fixture's unsafe label appears in a retrieved candidate set and whether the local rule-based engine marks it as passed. It does not measure whether an LLM follows the content or whether an attack succeeds in an agent system. A paper or presentation should call these synthetic scenario simulations until attack protocols and systems are independently implemented and documented.
