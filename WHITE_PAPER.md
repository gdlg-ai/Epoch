Project Epoch — Open-Source PoC White Paper (v0.2, concise)

Vision
- From passive assistant to digital symbiont: a privacy-first personal AI with lifelong memory, proactive help, and task execution.

Principles
- Privacy-first (local by default), Fully open-source (Apache-2.0), Hardware-agnostic (PoC), Community-driven.

PoC Goals
- Build a continuous personal memory loop (text-first; audio/vision to follow)
- Local RAG over personal memory
- Initial multimodal intake path (image→caption→memory)
- Run on accessible consumer hardware (PC/RPi/Jetson)

Tech Stack (first cut)
- ASR: Whisper/faster-whisper (planned)
- Embeddings: sentence-transformers (MiniLM/BGE)
- Vector store: JSONL now → ChromaDB/Weaviate next
- LLM/VLM: via Ollama (Phi-3, Mistral, LLaVA/Qwen-VL) later
- Backend: FastAPI, Frontend: Gradio, Orchestration: Docker Compose

Roadmap
- Phase 1 (Chronicler): perfect memory pipeline + daily digest
- Phase 2 (Librarian): VLM intake; model routing; deep RAG
- Phase 3 (Valet): agent tool-calls; proactive nudging

Ethics
- Explicit consent, transparency, local control, and options for digital rest (avoid over-reliance).

This PoC is a starting point, inviting contributions to turn the vision into an open ecosystem.
