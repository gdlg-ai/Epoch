Architecture (PoC — v0.2)

Scope: a minimal, local-first pipeline proving the memory loop and a simple UI. Default storage is an embedded vector DB; JSONL remains as a fallback.

Layers
- Capture: start with manual text input (audio now supported via local ASR; vision later)
- Memory: Vector DB (Chroma, embedded, persistent) with embeddings (BGE-small-zh) + cosine search
- Cognition: placeholder (LLM via Ollama in later iterations)
- Interface: FastAPI backend + Gradio UI

Data Flow
- /ingest: text (+tags, +source, +ts) → embed → write to vector store (Chroma) [default] or append JSONL [fallback]
- /query: query → embed → vector candidates → optional BM25 candidates → MMR diversification → top-k results

Services
- api: FastAPI, endpoints `/health`, `/ingest`, `/query`, `/asr`
- ui: Gradio client calling the API
- ollama: prepared but disabled for now (enable in compose as needed)

Next Steps
- Harden vector storage (Chroma) and export/import; consider Weaviate later if needed
- Add ASR pipeline (Whisper/faster-whisper) and VAD
- Add VLM intake (e.g., LLaVA/Qwen-VL) for images → text memory
- Introduce a prompt/RAG layer using local LLMs via Ollama
- Add Router (small/large/remote) and tool-calls for agents

Bilingual Documents
- zh-CN version: `docs/architecture.zh-CN.md`

Design Tenets
- Privacy-first: local by default, minimal/explicit egress.
- Composable: swappable ASR/Embedding/DB/LLM via clean interfaces.
- Minimal-yet-useful: prefer simple, observable pipelines over complexity.

Data Model (PoC)
- Record: `id` (uuid), `ts` (ISO), `source` (e.g., ui/api), `modality` (text|audio|image), `text`, `tags` (string[]), `embedding` (float[]), `meta` (object, optional).
- Storage: Vector DB (Chroma) with local persistence (default). Fallback: JSONL append-only. Storage behind a thin interface for swapping engines.

API Contract (current)
- `GET /health` → `{ "status":"ok", "items": number }`
- `POST /ingest` body: `{ text: string, tags?: string[], source?: string, ts?: string }` → `{ ok: boolean, id?: string }`
- `POST /query` body: `{ query: string, top_k?: number }` → `{ results: [{ text, tags, ts, score }] }`
- `POST /asr` form-data: `file: <audio>` → `{ language, text, segments: [{start,end,text}] }`

Configuration
- Embedding model: env (default `EMBED_MODEL=BAAI/bge-small-zh-v1.5`); BGE query prefix enabled.
- Device/runtime: CPU by default; GPU optional when available.
- Store type: `VECTOR_STORE=chroma` (default), fallback `jsonl`.
- Chroma persistence: `CHROMA_PERSIST_DIR=/app/data/chroma`, telemetry off by default.

Operations
- Local run: `docker compose up --build` then open `http://localhost:7860`.
- Data location: PoC JSONL lives under the api service’s data path (implementation detail, subject to change with vector DB).
- Export/Import: planned; index rebuild command to be added with vector DB.

Metrics & Benchmarks (targets)
- RAG latency (CPU): P50 < 400ms / P95 < 1000ms (query end-to-end, reranker OFF)
- Retrieval quality: Recall@5 ≥ 80% on small local eval; MRR@10 +0.1 with reranker vs baseline
- Footprint: runnable on consumer hardware without dedicated GPUs.

Retrieval Strategy
- Baseline: dense embeddings + cosine.
- Diversity: enable Maximal Marginal Relevance (MMR) post-filter on candidates.
- Hybrid (planned): add BM25 lexical index (Whoosh/Pyserini) and merge with dense results.

Modules (api)
- `services/api/embeddings.py` — embedding wrapper with BGE query prefix.
- `services/api/vector_store.py` — storage interface + Chroma adapter.
- `services/api/retrieval/hybrid.py` — BM25 tokenizer/index + MMR utility.
- `services/api/retrieval/rerank.py` — optional cross-encoder reranker (disabled by default).
- `services/api/asr.py` — faster-whisper integration (small/base, VAD).

Migration Plan (vector DB)
- Step 1: introduce storage interface; keep JSONL adapter.
- Step 2: add ChromaDB adapter; parity tests; migration script.
- Step 3: optional Weaviate adapter; router-based configuration.

Security & Privacy
- Local-first defaults; no network calls unless explicitly configured.
- Auditability: log ingest/query events locally with minimal metadata.

Related
- Vision: `docs/vision.md`

Hardware Profiles (quick guide)
- Minimum PoC (CPU-only): 2 cores, 4 GB RAM — text ingest/query.
- Recommended Dev: 8 cores, 16 GB RAM — target P50 < 2s.
- Workstation (GPU): 12+ cores, 32 GB RAM, ≥8–24 GB VRAM for larger LLMs.
- macOS: run API/UI in Docker; use Ollama on host for LLMs.
