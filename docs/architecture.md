Architecture (PoC — First Cut)

Scope: a minimal, local-first pipeline proving the memory loop and a simple UI.

Layers
- Capture: start with manual text input (audio/vision to be added)
- Memory: JSONL store + embeddings (sentence-transformers) + cosine search
- Cognition: placeholder (LLM via Ollama in later iterations)
- Interface: FastAPI backend + Gradio UI

Data Flow
- /ingest: text (+tags) → append to JSONL → embed → in-memory index
- /query: query → embed → cosine similarity → top-k results

Services
- api: FastAPI, endpoints `/health`, `/ingest`, `/query`
- ui: Gradio client calling the API
- ollama: prepared but disabled for now (enable in compose as needed)

Next Steps
- Replace JSONL with a vector DB (e.g., ChromaDB/Weaviate)
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
- Storage: JSONL at runtime (append-only). Planned: vector DB backend behind a thin abstraction.

API Contract (current)
- `GET /health` → `{"status":"ok"}`
- `POST /ingest` body: `{ text: string, tags?: string[], source?: string, ts?: string }` → `{ id: string }`
- `POST /query` body: `{ query: string, top_k?: number }` → `{ results: [{ id, text, tags, ts, score }] }`

Configuration
- Embedding model: env (e.g., `EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2`).
- Device/runtime: CPU by default; GPU optional when available.
- Store type: PoC JSONL; later `VECTOR_STORE=chroma|weaviate`.

Operations
- Local run: `docker compose up --build` then open `http://localhost:7860`.
- Data location: PoC JSONL lives under the api service’s data path (implementation detail, subject to change with vector DB).
- Export/Import: planned; index rebuild command to be added with vector DB.

Metrics & Benchmarks (targets)
- RAG latency P50 < 2s (end-to-end local; relaxed in early PoC).
- Retrieval quality: top-k hit-rate / subjective relevance ≥ 80% target.
- Footprint: runnable on consumer hardware without dedicated GPUs.

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
