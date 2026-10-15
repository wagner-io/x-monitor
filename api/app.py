import os
from functools import lru_cache
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

from indexer.embedder import Embedder
from indexer.faiss_store import FaissStore

app = FastAPI(title="X-Monitor Search API", version="1.0.0")


class SearchResult(BaseModel):
    score: float
    metadata: dict


class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]


@lru_cache
def resources() -> tuple[Embedder, FaissStore]:
    index_dir = os.getenv("INDEX_DIR", "data/index")
    if not (Path(index_dir) / "index.faiss").exists():
        raise FileNotFoundError(index_dir)
    return (
        Embedder(os.getenv("MODEL_DIR"), os.getenv("EMBEDDING_BACKEND", "hash"),
                 int(os.getenv("INDEX_DIM", "384"))),
        FaissStore.load(index_dir),
    )


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "X-Monitor Search API",
        "docs": "/docs",
        "health": "/health",
        "search": "/search?q=database%20timeout",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/search", response_model=SearchResponse)
def search(
    q: str = Query(min_length=1, description="Natural-language search query"),
    top_k: int = Query(default=5, ge=1, le=int(os.getenv("TOP_K_MAX", "20"))),
) -> SearchResponse:
    try:
        embedder, store = resources()
    except FileNotFoundError as exc:
        raise HTTPException(503, "Index unavailable") from exc
    results = [SearchResult(metadata=metadata, score=score)
               for metadata, score in store.search(embedder.embed([q])[0], top_k)]
    return SearchResponse(query=q, results=results)
