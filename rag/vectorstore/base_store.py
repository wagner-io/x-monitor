# rag/vectorstore/base_store.py

from abc import ABC, abstractmethod
import numpy as np

class VectorStore(ABC):
    """Abstrakte Basisklasse für alle Vectorstores."""

    @abstractmethod
    def index(self, embeddings: np.ndarray, metadatas: list[dict]):
        pass

    @abstractmethod
    def search(self, query_embedding: np.ndarray, top_k: int = 5):
        pass

    @abstractmethod
    def save(self, path: str):
        pass

    @abstractmethod
    def load(self, path: str):
        pass