"""Contract tests for concrete memory backend implementations."""

import hashlib

import pytest

from sentinelmem.backends import BackendRegistry, BaseMemoryBackend, EmulatedLangMemBackend, EmulatedMem0Backend, FAISSBackend, SearchResult
from sentinelmem.synthetic import load_synthetic_scenario


@pytest.mark.parametrize("backend", [FAISSBackend(), EmulatedMem0Backend(), EmulatedLangMemBackend()])
def test_backend_contract_write_search_delete_export_and_reset(backend):
    memories, queries = load_synthetic_scenario()
    selected = memories[0]
    ids = backend.write(selected, session_id="contract-session", agent_id="contract-agent")
    assert ids == [selected.record_id]
    assert backend.count() == 1
    assert isinstance(backend.search(queries[0].text, top_k=1)[0], SearchResult)
    stored = backend.list()[0]
    assert stored.source == selected.provenance
    assert stored.session_id == "contract-session"
    assert stored.agent_id == "contract-agent"
    assert stored.written_at is not None
    assert stored.content_hash == hashlib.sha256(stored.text.encode()).hexdigest()
    assert backend.export_state()[0]["content_hash"] == stored.content_hash
    assert backend.delete(selected.record_id) is True
    assert backend.delete(selected.record_id) is False
    backend.write(memories[:2])
    backend.reset()
    assert backend.count() == 0
    assert backend.list() == []


def test_backend_registry_names_emulators_explicitly():
    available = BackendRegistry.list_available()
    assert available == ["emulated_langmem", "emulated_mem0", "faiss"]
    assert isinstance(BackendRegistry.get("emulated_mem0"), EmulatedMem0Backend)
    assert isinstance(BackendRegistry.get("emulated_langmem"), EmulatedLangMemBackend)
    assert isinstance(BackendRegistry.get("faiss", embedding_dimension=32), BaseMemoryBackend)
    with pytest.raises(ValueError, match="Unknown backend"):
        BackendRegistry.get("mem0")
