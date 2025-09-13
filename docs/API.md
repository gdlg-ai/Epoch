API Reference (v0.2)

Base URL
- Default: `http://localhost:8000`

Endpoints
- `GET /health`
  - Returns: `{ "status": "ok", "items": number }`

- `GET /model`
  - Returns: a summary of current model/storage/retrieval/ASR settings, e.g.
    ```json
    {
      "embedding": {"model": "BAAI/bge-small-zh-v1.5", "add_query_prefix": "true"},
      "retrieval": {"top_k": 5, "use_mmr": true, "enable_bm25": true, "enable_reranker": false},
      "storage": {"backend": "chroma", "chroma_persist_dir": "/app/data/chroma"},
      "asr": {"enabled": "true", "size": "small", "device": "auto"}
    }
    ```

- `POST /ingest`
  - Body (JSON): `{ text: string, tags?: string[], source?: string, ts?: string }`
  - Returns: `{ ok: boolean, id?: string }`
  - Notes: When using the Chroma vector store (default), an internal `id` is generated.

- `POST /query`
  - Body (JSON): `{ query: string, top_k?: number }`
  - Returns: `{ results: [{ text: string, tags: string[], ts?: string, score: number }] }`
  - Notes: Results are diversified using MMR by default. BM25/hybrid and reranker can be toggled via env.

- `POST /asr`
  - Form-Data: `file=<audio>`
  - Returns: `{ language: string, text: string, segments: [{ start: number, end: number, text: string }] }`
  - Notes: Enabled when `ASR_ENABLED=true`. Uses faster-whisper small/base locally.

Environment Toggles (selection)
- Retrieval: `TOP_K`, `USE_MMR`, `ENABLE_BM25`, `ENABLE_RERANKER`
- Embeddings: `EMBED_MODEL`, `EMBED_ADD_QUERY_PREFIX`
- Storage: `VECTOR_STORE=chroma|jsonl`, `CHROMA_PERSIST_DIR`
