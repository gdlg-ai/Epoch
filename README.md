Project Epoch — Your Private, Personal AI (Open‑Source)

See Chinese version: `README.zh-CN.md`.

Epoch is a privacy‑first, local‑first personal AI that remembers for you, helps proactively, and can act on your behalf — and you own the data. Today it is a minimal, runnable PoC; our vision is a trustworthy “digital symbiont” that lives on your devices.

Why it matters
- Privacy you can verify: local by default, no surprise data egress.
- Your second brain: instantly recall conversations, notes, and images.
- From chat to actions: move beyond Q&A toward real task completion.
- Open and portable: Apache‑2.0, data export/import, community‑built.

Try It (2 minutes)
- Prerequisites: Docker + Docker Compose; optional GPU drivers
- Setup:
  - Copy `.env.example` to `.env` and adjust if needed
  - Start services: `docker compose up --build`
  - Open UI: http://localhost:7860

What you can do today
- Ingest short notes (text) and instantly search by meaning (semantic search).
- Explore a minimal UI and API that runs entirely on your machine.
- Inspect how we embed, store, and retrieve memories (transparent by design).

Roadmap
- Phase 1 — Chronicler: audio→ASR→embed→vector store→text RAG; daily digest
- Phase 2 — Librarian: image→VLM→memory; model routing; deeper retrieval
- Phase 3 — Valet: agent tool‑calls (calendar/web); proactive reminders

How it’s built (at a glance)
- `compose.yaml` — container orchestration
- `services/api` — FastAPI backend (ingest/query memory)
- `services/ui` — Gradio frontend
- `docs/` — architecture and white paper (EN + zh-CN)
 - See `docs/requirements.md` for system requirements and recommended configs

Vision & Architecture
- Vision: `docs/vision.md` (see zh-CN: `docs/vision.zh-CN.md`)
- Architecture: `docs/architecture.md` (see zh-CN: `docs/architecture.zh-CN.md`)
 - Investor Brief: `docs/investor_brief.md` (zh-CN: `docs/investor_brief.zh-CN.md`)
 - Deep Research Prompts: `docs/deep_research_prompts.md` (zh-CN: `docs/deep_research_prompts.zh-CN.md`)

Milestones
- v0.1 — Daily Review Loop (ingest → embed → store → retrieve → summarize)
- Next — Retrieval & latency baselines; vector DB migration behind an interface

Who this is for
- Individuals who want a private “second brain” they truly own.
- Teams with sensitive knowledge (legal, health, R&D) needing local‑first AI.
- Builders who prefer open, swappable components over closed black boxes.

Support the project
- Try the PoC and share feedback as issues.
- Star the repo to help visibility and community growth.
- Contribute modules (ASR/embeddings/vector DB/LLM tools) via PRs.
- Interested in partnerships or funding? Open a discussion — we’re building a trustworthy, open ecosystem for personal AI with a clear path from PoC → product.

License
Apache License 2.0. See `LICENSE`.

Contributing
- See `docs/architecture.md` and open issues.
- PRs welcome for: ASR pipeline, embeddings/vector DB integration, RAG prompts, VLM hookup, and agent tools.

FAQ
- Is my data private? Yes. Local by default, no network calls unless you opt in.
- Does it work offline? Yes. After initial image/model pulls, it runs offline.
- Do I need a GPU? No. CPU is fine for PoC; GPU speeds up ASR/LLM later.
- How is this different from cloud chatbots? You own the data, verifiable local-first, and we focus on memory + actions.
- What’s the business model? Open-core with optional enterprise features and partnerships.
 - Full FAQ: `docs/faq.md`

Bilingual Documents
- English: `README.md`, `docs/architecture.md`, `WHITE_PAPER.md`
- 中文: `README.zh-CN.md`, `docs/architecture.zh-CN.md`, `WHITE_PAPER.zh-CN.md`
 - System Requirements: `docs/requirements.md` (zh-CN: `docs/requirements.zh-CN.md`)
