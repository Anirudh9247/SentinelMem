import numpy as np

from sentinelmem.synthetic import deterministic_embedding, load_synthetic_scenario


def test_embedding_is_deterministic_and_normalized():
    first = deterministic_embedding("reproducible retrieval", 64)
    second = deterministic_embedding("reproducible retrieval", 64)

    assert np.array_equal(first, second)
    assert np.isclose(np.linalg.norm(first), 1.0)


def test_scenario_has_trusted_and_untrusted_memories():
    memories, queries = load_synthetic_scenario()

    assert len(memories) == 12
    assert len(queries) == 4
    assert {memory.label for memory in memories} == {"benign", "instruction_shaped"}
