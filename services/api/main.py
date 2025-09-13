import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


APP_ENV = os.getenv("APP_ENV", "dev")
MEMORY_PATH = Path(os.getenv("MEMORY_PATH", "/app/data/memory.jsonl"))
EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-small-zh-v1.5")
DEFAULT_TOP_K = int(os.getenv("TOP_K", "5"))
USE_MMR = os.getenv("USE_MMR", "true").lower() == "true"
MMR_CANDIDATES = int(os.getenv("MMR_CANDIDATES", "20"))
MMR_LAMBDA = float(os.getenv("MMR_LAMBDA", "0.5"))


class IngestItem(BaseModel):
    text: str
    tags: Optional[List[str]] = None
    ts: Optional[str] = None  # ISO timestamp optional
    source: Optional[str] = None  # e.g., ui/api


class QueryItem(BaseModel):
    query: str
    top_k: int = DEFAULT_TOP_K


class MemoryStore:
    def __init__(self, path: Path):
        self.path = path
        self.model: Optional[SentenceTransformer] = None
        self._texts: List[str] = []
        self._tags: List[List[str]] = []
        self._ts: List[Optional[str]] = []
        self._emb: Optional[np.ndarray] = None
        self._ensure_file()
        self._load()

    def _ensure_file(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.touch()

    def _lazy_model(self):
        if self.model is None:
            # Lightweight, widely-available embedding model (configurable)
            self.model = SentenceTransformer(EMBED_MODEL)
        return self.model

    def _load(self):
        self._texts.clear()
        self._tags.clear()
        self._ts.clear()
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                self._texts.append(obj.get("text", ""))
                self._tags.append(obj.get("tags", []) or [])
                self._ts.append(obj.get("ts"))
        if self._texts:
            emb = self._lazy_model().encode(self._texts, convert_to_numpy=True, normalize_embeddings=True)
            self._emb = emb
        else:
            self._emb = None

    def ingest(self, text: str, tags: Optional[List[str]] = None, ts: Optional[str] = None, source: Optional[str] = None):
        if ts is None:
            ts = datetime.now(timezone.utc).isoformat()
        obj = {"text": text, "tags": tags or [], "ts": ts, "source": source}
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        # Update in-memory state
        self._texts.append(text)
        self._tags.append(tags or [])
        self._ts.append(ts)
        vec = self._lazy_model().encode([text], convert_to_numpy=True, normalize_embeddings=True)
        if self._emb is None:
            self._emb = vec
        else:
            self._emb = np.vstack([self._emb, vec])

    def query(self, query: str, top_k: int = DEFAULT_TOP_K):
        if not self._texts:
            return []
        q = self._lazy_model().encode([query], convert_to_numpy=True, normalize_embeddings=True)
        sims = cosine_similarity(q, self._emb)[0]
        # Initial candidate pool
        if USE_MMR:
            k_cand = min(MMR_CANDIDATES, len(sims))
            cand_idx = np.argsort(-sims)[:k_cand]
            selected = []
            # Precompute candidate-candidate similarities for MMR
            cand_vecs = self._emb[cand_idx]
            # Normalize should be already true; cosine sim equals dot product
            cand_sims = cosine_similarity(cand_vecs, cand_vecs)
            # Query-candidate sims
            q_sims = sims[cand_idx]
            while len(selected) < min(top_k, k_cand):
                if not selected:
                    # pick the best by relevance
                    next_i = int(np.argmax(q_sims))
                else:
                    # compute MMR score = lambda*rel - (1-lambda)*max_sim_to_selected
                    max_sim_to_sel = cand_sims[:, selected].max(axis=1)
                    mmr_scores = MMR_LAMBDA * q_sims - (1 - MMR_LAMBDA) * max_sim_to_sel
                    # Mask already selected
                    mmr_scores[selected] = -1e9
                    next_i = int(np.argmax(mmr_scores))
                selected.append(next_i)
            final_idx = cand_idx[selected]
        else:
            final_idx = np.argsort(-sims)[:top_k]
        results = []
        for i in final_idx:
            results.append({
                "text": self._texts[i],
                "tags": self._tags[i],
                "ts": self._ts[i],
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
    store.ingest(item.text, item.tags, item.ts, item.source)
    return {"ok": True}


@app.post("/query")
def query(item: QueryItem):
    results = store.query(item.query, item.top_k)
    return {"results": results}
