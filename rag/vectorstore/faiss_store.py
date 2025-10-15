# rag/vectorstore/faiss_store.py

import faiss
import numpy as np
import pickle
from .base_store import VectorStore

class FAISSStore(VectorStore):
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.metadatas = []

    def index(self, embeddings: np.ndarray, metadatas: list[dict]):
        self.index.add(embeddings) 
        self.metadatas.extend(metadatas)

    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        D, I = self.index.search(query_embedding, top_k)
        return [(self.metadatas[i], float(D[0][idx])) for idx, i in enumerate(I[0])]

    def save(self, path: str):
        faiss.write_index(self.index, f"{path}/index.faiss")
        with open(f"{path}/meta.pkl", "wb") as f:
            pickle.dump(self.metadatas, f)

    def load(self, path: str):
        self.index = faiss.read_index(f"{path}/index.faiss")
        with open(f"{path}/meta.pkl", "rb") as f:
            self.metadatas = pickle.load(f)