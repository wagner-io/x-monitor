import os
from datetime import datetime
from s3_accessor import S3Accessor
from embedder import Embedder
from faiss_store import FaissStore
from metadata_builder import build_metadata

def main():
    bucket = os.environ.get("DATA_BUCKET", "x-monitor-data")
    model_dir = os.environ.get("MODEL_DIR", "/app/model")
    output_dir = os.environ.get("OUTPUT_DIR", "/tmp/faiss")

    print(f"[{datetime.now()}] Starte Indexaufbau für Bucket {bucket}")

    s3 = S3Accessor(bucket)
    embedder = Embedder(model_dir)
    store = FaissStore(dim=384)

    # 1️⃣ Texte laden
    keys = s3.list_objects("logs/")
    texts = [s3.get_object_text(k) for k in keys]

    # 2️⃣ Embeddings erzeugen
    embeddings = embedder.embed(texts)

    # 3️⃣ In Index speichern
    metadata = [{"s3_key": k} for k in keys]
    store.add_vectors(embeddings, metadata)
    store.save(output_dir)

    print(f"✅ Index erfolgreich erstellt ({len(keys)} Dokumente).")

if __name__ == "__main__":
    main()