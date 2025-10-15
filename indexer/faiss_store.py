import faiss
import json
import numpy as np
import os

class FaissStore:
    """Verwaltet den FAISS Index und Metadaten."""

    def __init__(self, dim: int = 384):
        self.index = faiss.IndexFlatIP(dim)
        self.metadatas = []

    def add_vectors(self, embeddings: np.ndarray, metadata: list[dict]):
        faiss.normalize_L2(embeddings)
        self.index.add(embeddings.astype(np.float32))
        self.metadatas.extend(metadata)

    def save(self, path: str):
        os.makedirs(path, exist_ok=True)
        faiss.write_index(self.index, f"{path}/index.faiss")
        with open(f"{path}/meta.json", "w") as f:
            json.dump(self.metadatas, f, indent=2)
        print(f"✅ FAISS Index gespeichert unter {path}/")