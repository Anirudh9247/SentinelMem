"""Tests for SentinelMem attack suite."""

from sentinelmem.attacks import DirectWriteAttack, MINJAAttack, SleeperAttack
from sentinelmem.backends import FAISSBackend


def test_minja_attack_payloads_and_queries():
    attack = MINJAAttack()
    assert attack.name == "minja_query_injection"
    payloads = attack.generate_payloads()
    queries = attack.generate_eval_queries()

    assert len(payloads) == 4
    assert all(p.label == "instruction_shaped" for p in payloads)
    assert len(queries) == 4

    backend = FAISSBackend(embedding_dimension=64)
    injected_ids = attack.execute(backend)
    assert len(injected_ids) == 4
    assert backend.count() == 4


def test_sleeper_and_direct_write_attacks():
    sleeper = SleeperAttack()
    assert len(sleeper.generate_payloads()) == 2
    assert len(sleeper.generate_eval_queries()) == 2

    direct = DirectWriteAttack()
    assert len(direct.generate_payloads()) == 2
    assert len(direct.generate_eval_queries()) == 2
