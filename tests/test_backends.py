"""Unit tests for SentinelMem backend adapters and registry."""

import pytest

from sentinelmem.backends import BackendRegistry, BaseMemoryBackend, FAISSBackend, SearchResult
from sentinelmem.synthetic import MemoryRecord, deterministic_embedding, load_synthetic_scenario


def test_faiss_backend_lifecycle():
    backend = FAISSBackend(embedding_dimension=64)
    assert backend.name == "faiss"
    assert backend.count() == 0

    memories, queries = load_synthetic_scenario()
    inserted_ids = backend.add(memories)
    
    assert len(inserted_ids) == len(memories)
    assert backend.count() == len(memories)

    # Search top 3
    results = backend.search(queries[0].text, top_k=3)
    assert len(results) == 3
    assert isinstance(results[0], SearchResult)
    assert results[0].score >= results[1].score >= results[2].score

    # Batch search
    batch_results = backend.search_batch([q.text for q in queries], top_k=3)
    assert len(batch_results) == len(queries)
    for res in batch_results:
        assert len(res) == 3

    # Clear
    backend.clear()
    assert backend.count() == 0
    assert backend.search("query", top_k=3) == []


def test_backend_registry():
    available = BackendRegistry.list_available()
    assert "faiss" in available

    backend = BackendRegistry.get("faiss", embedding_dimension=32)
    assert isinstance(backend, BaseMemoryBackend)
    assert backend.name == "faiss"
    assert backend.embedding_dimension == 32

    with pytest.raises(ValueError, match="Unknown backend"):
        BackendRegistry.get("nonexistent_backend")
