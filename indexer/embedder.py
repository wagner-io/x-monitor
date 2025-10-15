from sentence_transformers import SentenceTransformer
import numpy as np

class Embedder:
    """Kapselt das Embedding-Modell (SentenceTransformer)."""

    def __init__(self, model_dir: str):
        print(f"🧠 Lade Modell aus {model_dir} ...")
        self.model = SentenceTransformer(model_dir)
        print("✅ Modell geladen.")

    def embed(self, texts: list[str]) -> np.ndarray:
        """Berechnet Embeddings für eine Liste von Texten."""
        return self.model.encode(
            texts, batch_size=64, convert_to_numpy=True, show_progress_bar=False
        )