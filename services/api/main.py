import json
import os
from pathlib import Path
from typing import List, Optional

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


APP_ENV = os.getenv("APP_ENV", "dev")
MEMORY_PATH = Path(os.getenv("MEMORY_PATH", "/app/data/memory.jsonl"))


class IngestItem(BaseModel):
    text: str
    tags: Optional[List[str]] = None


class QueryItem(BaseModel):
    query: str
    top_k: int = 5


class MemoryStore:
    def __init__(self, path: Path):
        self.path = path
        self.model: Optional[SentenceTransformer] = None
        self._texts: List[str] = []
        self._tags: List[List[str]] = []
        self._emb: Optional[np.ndarray] = None
        self._ensure_file()
        self._load()

    def _ensure_file(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()

    def _lazy_model(self):
        if self.model is None:
            # Lightweight, widely-available embedding model
            self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        return self.model

    def _load(self):
        self._texts.clear()
        self._tags.clear()
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                self._texts.append(obj.get("text", ""))
                self._tags.append(obj.get("tags", []) or [])
        if self._texts:
            emb = self._lazy_model().encode(self._texts, convert_to_numpy=True, normalize_embeddings=True)
            self._emb = emb
        else:
            self._emb = None

    def ingest(self, text: str, tags: Optional[List[str]] = None):
        obj = {"text": text, "tags": tags or []}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        # Update in-memory state
        self._texts.append(text)
        self._tags.append(tags or [])
        vec = self._lazy_model().encode([text], convert_to_numpy=True, normalize_embeddings=True)
        if self._emb is None:
            self._emb = vec
        else:
            self._emb = np.vstack([self._emb, vec])

    def query(self, query: str, top_k: int = 5):
        if not self._texts:
            return []
        q = self._lazy_model().encode([query], convert_to_numpy=True, normalize_embeddings=True)
        sims = cosine_similarity(q, self._emb)[0]
        idx = np.argsort(-sims)[:top_k]
        results = []
        for i in idx:
            results.append({
                "text": self._texts[i],
                "tags": self._tags[i],
                "score": float(sims[i])
            })
        return results


store = MemoryStore(MEMORY_PATH)
app = FastAPI(title="Epoch API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok", "items": len(store._texts)}


@app.post("/ingest")
def ingest(item: IngestItem):
    store.ingest(item.text, item.tags)
    return {"ok": True}


@app.post("/query")
def query(item: QueryItem):
    results = store.query(item.query, item.top_k)
    return {"results": results}

