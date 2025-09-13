Project Epoch — Open-Source PoC White Paper (v0.2, concise)

Vision
- From passive assistant to digital symbiont: a privacy-first personal AI with lifelong memory, proactive help, and task execution.

Principles
- Privacy-first (local by default), Fully open-source (Apache-2.0), Hardware-agnostic (PoC), Community-driven.

PoC Goals (updated)
- Build a continuous personal memory loop (text-first; audio added; vision to follow)
- Local RAG over personal memory with an embedded vector DB (Chroma)
- Initial multimodal intake path (image→caption→memory)
- Run on accessible consumer hardware (PC/RPi/Jetson)

Tech Stack (v0.2)
- ASR: faster-whisper (small/base) local, with VAD
- Embeddings: BGE-small-zh (default; CPU-friendly), BGE-M3 optional (GPU recommended)
- Vector store: ChromaDB (embedded, persistent, offline) default; JSONL fallback
- LLM/VLM: via Ollama (Phi-3, Mistral, LLaVA/Qwen-VL) later
- Backend: FastAPI; Frontend: Gradio; Orchestration: Docker Compose

Roadmap
- Phase 1 (Chronicler): memory pipeline with vector DB + daily digest; evaluation baselines
- Phase 2 (Librarian): VLM intake; model routing; hybrid retrieval and reranking
- Phase 3 (Valet): agent tool-calls; proactive nudging

Ethics
- Explicit consent, transparency, local control, and options for digital rest (avoid over-reliance).

This PoC is a starting point, inviting contributions to turn the vision into an open ecosystem.

Appendix
- FAQ: `docs/faq.md`
