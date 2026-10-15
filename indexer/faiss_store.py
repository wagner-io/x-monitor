import json
from pathlib import Path

import faiss
import numpy as np


class FaissStore:
    """Cosine-similarity index with JSON metadata."""

    def __init__(self, dim: int = 384):
        self.index = faiss.IndexFlatIP(dim)
        self.metadatas: list[dict] = []

    def add_vectors(self, embeddings: np.ndarray, metadata: list[dict]) -> None:
        vectors = np.asarray(embeddings, dtype=np.float32).copy()
        faiss.normalize_L2(vectors)
        self.index.add(vectors)
        self.metadatas.extend(metadata)

    def search(self, embedding: np.ndarray, top_k: int = 5) -> list[tuple[dict, float]]:
        if not self.metadatas:
            return []
        query = np.asarray(embedding, dtype=np.float32).reshape(1, -1).copy()
        faiss.normalize_L2(query)
        scores, indices = self.index.search(query, min(top_k, len(self.metadatas)))
        return [(self.metadatas[i], float(scores[0][pos])) for pos, i in enumerate(indices[0]) if i >= 0]

    def save(self, path: str) -> None:
        target = Path(path)
        target.mkdir(parents=True, exist_ok=True)
        faiss.write_index(self.index, str(target / "index.faiss"))
        (target / "meta.json").write_text(json.dumps(self.metadatas, indent=2, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def load(cls, path: str) -> "FaissStore":
        source = Path(path)
        store = cls(faiss.read_index(str(source / "index.faiss")).d)
        store.index = faiss.read_index(str(source / "index.faiss"))
        store.metadatas = json.loads((source / "meta.json").read_text(encoding="utf-8"))
        return store
