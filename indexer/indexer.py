import os
from datetime import datetime, timezone

from .embedder import Embedder
from .faiss_store import FaissStore
from .s3_accessor import S3Accessor


def main() -> None:
    bucket = os.getenv("DATA_BUCKET", "x-monitor-data")
    prefix = os.getenv("S3_PREFIX", "logs/")
    output_dir = os.getenv("OUTPUT_DIR", "data/index")
    backend = os.getenv("EMBEDDING_BACKEND", "sentence-transformers")
    model_dir = os.getenv("MODEL_DIR", "/app/model")
    dimensions = int(os.getenv("INDEX_DIM", "384"))

    print(f"[{datetime.now(timezone.utc).isoformat()}] Building index for {bucket}/{prefix}")
    s3 = S3Accessor(bucket)
    keys = s3.list_objects(prefix)
    texts = [s3.get_object_text(key) for key in keys]
    embedder = Embedder(model_dir, backend, dimensions)
    store = FaissStore(dim=dimensions)
    store.add_vectors(embedder.embed(texts), [{"s3_key": key, "text": text} for key, text in zip(keys, texts)])
    store.save(output_dir)
    print(f"Index created: {len(keys)} documents")


if __name__ == "__main__":
    main()
