from indexer.embedder import Embedder
from indexer.faiss_store import FaissStore
from indexer.metadata_builder import build_metadata


def test_metadata_builds_every_item():
    docs, metadata = build_metadata([
        {"id": "a", "type": "log", "message": "timeout"},
        {"id": "b", "type": "event", "detail": "deploy"},
    ])
    assert len(docs) == len(metadata) == 2
    assert "timeout" in docs[0]


def test_store_round_trip(tmp_path):
    embedder = Embedder(dimensions=8)
    store = FaissStore(dim=8)
    store.add_vectors(embedder.embed(["database timeout", "successful deploy"]), [{"id": "1"}, {"id": "2"}])
    store.save(str(tmp_path))
    loaded = FaissStore.load(str(tmp_path))
    assert loaded.search(embedder.embed(["database timeout"])[0], 1)[0][0]["id"] == "1"
