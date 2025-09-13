API Reference (v0.2)

Base URL
- Default: `http://localhost:8000`

Endpoints
- `GET /health`
  - Returns: `{ "status": "ok", "items": number }`

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

