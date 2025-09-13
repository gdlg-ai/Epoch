import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict

import numpy as np
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from uuid import uuid4

from services.api.embeddings import EmbeddingModel
from services.api.vector_store import get_vector_store, VectorStore as VS
from services.api.retrieval.hybrid import BM25Index, mmr
from services.api.retrieval.rerank import CrossEncoderReranker


APP_ENV = os.getenv("APP_ENV", "dev")
MEMORY_PATH = Path(os.getenv("MEMORY_PATH", "/app/data/memory.jsonl"))
EMBED_MODEL = os.getenv("EMBED_MODEL", "BAAI/bge-small-zh-v1.5")
DEFAULT_TOP_K = int(os.getenv("TOP_K", "5"))
USE_MMR = os.getenv("USE_MMR", "true").lower() == "true"
MMR_CANDIDATES = int(os.getenv("MMR_CANDIDATES", "20"))
MMR_LAMBDA = float(os.getenv("MMR_LAMBDA", "0.5"))
ENABLE_BM25 = os.getenv("ENABLE_BM25", "true").lower() == "true"
ENABLE_RERANKER = os.getenv("ENABLE_RERANKER", "false").lower() == "true"


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

# Global state
store = MemoryStore(MEMORY_PATH)
embedder = EmbeddingModel()
vector_store: Optional[VS] = None
bm25_index: Optional[BM25Index] = None
bm25_ids: List[str] = []
bm25_texts: List[str] = []
corpus_map: Dict[str, Dict] = {}
try:
    if os.getenv("VECTOR_STORE", "jsonl").lower() == "chroma":
        vector_store = get_vector_store()
except Exception as _e:
    vector_store = None
reranker = CrossEncoderReranker() if ENABLE_RERANKER else None

app = FastAPI(title="Epoch API", version="0.2.0")


@app.get("/health")
def health():
    cnt = vector_store.count() if vector_store is not None else len(store._texts)
    return {"status": "ok", "items": cnt}


@app.post("/ingest")
def ingest(item: IngestItem):
    # Generate id and timestamp if not provided
    ts = item.ts or datetime.now(timezone.utc).isoformat()
    if vector_store is not None:
        doc_id = uuid4().hex
        vec = embedder.embed_docs([item.text])[0]
        meta = {"tags": item.tags or [], "ts": ts, "source": item.source or "api"}
        vector_store.add([
            {"id": doc_id, "text": item.text, "embedding": vec, "meta": meta}
        ])
        # BM25 snapshot
        if ENABLE_BM25:
            bm25_ids.append(doc_id)
            bm25_texts.append(item.text)
            corpus_map[doc_id] = {"text": item.text, "meta": meta}
        return {"ok": True, "id": doc_id}
    else:
        store.ingest(item.text, item.tags, ts, item.source)
        return {"ok": True}


@app.post("/query")
def query(item: QueryItem):
    if vector_store is None:
        results = store.query(item.query, item.top_k)
        return {"results": results}
    # Vector candidates (oversample for MMR)
    oversample = max(item.top_k * 3, min(MMR_CANDIDATES, item.top_k * 4))
    qvec = np.array(embedder.embed_query(item.query), dtype="float32")
    vec_hits = vector_store.query(qvec.tolist(), top_k=oversample)
    # Optional BM25
    merged: Dict[str, Dict] = {}
    for h in vec_hits:
        merged[h["id"]] = {"id": h["id"], "text": h["text"], "meta": h.get("meta", {}), "score": h.get("score", 0.0)}
        corpus_map.setdefault(h["id"], {"text": h["text"], "meta": h.get("meta", {})})
        if ENABLE_BM25 and h["id"] not in bm25_ids:
            bm25_ids.append(h["id"])
            bm25_texts.append(h["text"])
    if ENABLE_BM25 and bm25_texts and bm25_ids:
        global bm25_index
        if bm25_index is None or len(bm25_ids) != len(getattr(bm25_index, "ids", [])):
            bm25_index = BM25Index(bm25_texts, bm25_ids)
        for bid, bscore in bm25_index.search(item.query, top_k=oversample):
            if bid not in merged:
                meta = corpus_map.get(bid, {}).get("meta", {})
                text = corpus_map.get(bid, {}).get("text", "")
                merged[bid] = {"id": bid, "text": text, "meta": meta, "score": 0.0, "bm25": bscore}
            else:
                merged[bid]["bm25"] = bscore
    candidates = list(merged.values())[:oversample]
    # MMR diversification
    if USE_MMR and candidates:
        doc_vecs = np.array([embedder.embed_docs([c["text"]])[0] for c in candidates], dtype="float32")
        # normalize
        doc_vecs = doc_vecs / (np.linalg.norm(doc_vecs, axis=1, keepdims=True) + 1e-9)
        qn = qvec / (np.linalg.norm(qvec) + 1e-9)
        sel_idx = mmr(qn, doc_vecs, top_k=item.top_k, lambda_mult=MMR_LAMBDA)
        selected = [candidates[i] for i in sel_idx]
    else:
        # fallback to top by vector score
        selected = sorted(candidates, key=lambda x: x.get("score", 0.0), reverse=True)[: item.top_k]
    # Optional rerank
    if ENABLE_RERANKER and selected:
        try:
            scores = reranker.score(item.query, [c["text"] for c in selected])
            selected = [x for _, x in sorted(zip(scores, selected), key=lambda t: t[0], reverse=True)]
        except Exception:
            pass
    # Format
    out = []
    for c in selected[: item.top_k]:
        meta = c.get("meta", {})
        out.append(
            {
                "text": c.get("text", ""),
                "tags": meta.get("tags", []),
                "ts": meta.get("ts"),
                "score": float(c.get("score", 0.0)),
            }
        )
    return {"results": out}


@app.post("/asr")
def asr(file: UploadFile = File(...)):
    if os.getenv("ASR_ENABLED", "true").lower() != "true":
        raise HTTPException(status_code=400, detail="ASR disabled")
    from services.api.asr import ASR  # lazy import

    tmp_path = f"/tmp/{file.filename}"
    with open(tmp_path, "wb") as f:
        f.write(file.file.read())
    asr_engine = ASR()
    try:
        res = asr_engine.transcribe(tmp_path, vad=os.getenv("ASR_VAD_FILTER", "true").lower() == "true")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return res
