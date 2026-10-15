import hashlib
from pathlib import Path

import numpy as np


class Embedder:
    """Embedding adapter: deterministic demo backend or Sentence Transformers."""

    def __init__(self, model_dir: str | None = None, backend: str = "hash", dimensions: int = 384):
        self.backend = backend
        self.dimensions = dimensions
        self.model = None
        if backend == "sentence-transformers":
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_dir or str(Path("./data/model")))

    def embed(self, texts: list[str]) -> np.ndarray:
        if self.model is not None:
            vectors = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
            return vectors.astype(np.float32)
        vectors = np.zeros((len(texts), self.dimensions), dtype=np.float32)
        for row, text in enumerate(texts):
            for token in text.lower().split():
                digest = hashlib.sha256(token.encode("utf-8")).digest()
                bucket = int.from_bytes(digest[:8], "little") % self.dimensions
                vectors[row, bucket] += 1.0
            norm = np.linalg.norm(vectors[row])
            if norm:
                vectors[row] /= norm
        return vectors
