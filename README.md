Project Epoch (Open-Source PoC)

Bilingual docs available: see `README.zh-CN.md`.

Project Epoch is an open-source, privacy-first personal AI companion PoC. It aims to validate a minimal end-to-end loop for personal memory: capture → transcribe → embed → store → retrieve (RAG) → respond, with a simple UI and local services.

This repo provides a minimal, runnable skeleton to start iterating quickly and transparently.

Quick Start
- Prerequisites: Docker + Docker Compose; optional GPU drivers
- Setup:
  - Copy `.env.example` to `.env` and adjust if needed
  - Start services: `docker compose up --build`
  - Open UI: http://localhost:7860

Services (first cut)
- `api` (FastAPI): basic memory ingest/query, simple RAG stub
- `ui` (Gradio): minimal UI for ingest + query
- `ollama` (prepared): local LLM/VLM runtime (disabled in first cut)

Roadmap (PoC)
- Phase 1 (Chronicler): audio→ASR→embed→vector-store→text RAG; daily digest
- Phase 2 (Librarian): image→VLM→memory; model routing; deeper RAG
- Phase 3 (Valet): agent tool-calls (calendar/web); proactive nudging

Repo Structure
- `compose.yaml` — container orchestration
- `services/api` — FastAPI backend (ingest/query memory)
- `services/ui` — Gradio frontend
- `docs/` — architecture and white paper (EN + zh-CN)

License
Apache License 2.0. See `LICENSE`.

Contributing
- See `docs/architecture.md` and open issues.
- PRs welcome for: ASR pipeline, embeddings/vector DB integration, RAG prompts, VLM hookup, and agent tools.

Bilingual Documents
- English: `README.md`, `docs/architecture.md`, `WHITE_PAPER.md`
- 中文: `README.zh-CN.md`, `docs/architecture.zh-CN.md`, `WHITE_PAPER.zh-CN.md`
