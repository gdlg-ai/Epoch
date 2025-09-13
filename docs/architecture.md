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
