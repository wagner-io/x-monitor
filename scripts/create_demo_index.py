from pathlib import Path

from indexer.embedder import Embedder
from indexer.faiss_store import FaissStore
from indexer.metadata_builder import build_metadata

ITEMS = [
    {"id": "1", "type": "log", "timestamp": "2026-01-10T10:00:00Z", "source": "api", "message": "database connection timeout", "service": "checkout"},
    {"id": "2", "type": "event", "timestamp": "2026-01-10T10:02:00Z", "service": "payments", "detail": "deployment completed successfully"},
    {"id": "3", "type": "cost", "date": "2026-01-10", "service": "Amazon S3", "region": "eu-central-1", "cost": "12.40"},
]


def main() -> None:
    texts, metadata = build_metadata(ITEMS)
    embedder = Embedder(backend="hash")
    store = FaissStore(dim=384)
    store.add_vectors(embedder.embed(texts), metadata)
    store.save("data/index")
    print("Demo index written to data/index")


if __name__ == "__main__":
    main()
