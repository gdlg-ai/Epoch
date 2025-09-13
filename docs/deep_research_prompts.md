OpenAI Deep Research — Prompt Pack (Project Epoch v0.2)

Global Instructions (paste at top of each task)
- Scope: privacy-first, local-first, consumer hardware (CPU-first; optional NVIDIA GPU), bilingual EN/zh, open-source friendly licenses.
- Output: executive summary; recommendation; options/trade-offs matrix; step-by-step implementation plan; risks; benchmarks (latency/quality); citations with URLs.
- Constraints: offline-capable; small/medium models preferred (<= 8–13GB VRAM); CPU viability required; permissive/commercial-friendly licenses.
- Deliverables: PR-ready doc updates, env/config defaults, interface outlines, evaluation script plan.
- Acceptance: recommendations must map to specific repo files with estimated effort and risks.

Context Snapshot (current repo)
- PoC loop: ingest (text) → embed (MiniLM) → JSONL store → cosine search → UI response.
- Backend/UI: FastAPI (services/api), Gradio UI (services/ui), Docker Compose with optional `ollama` profile.
- Embeddings: default `sentence-transformers/all-MiniLM-L6-v2` configurable via `EMBED_MODEL`.
- API: `/health`, `/ingest` (supports optional `ts`/`source`), `/query` (returns `ts`, supports `TOP_K`).
- Docs: Bilingual vision, architecture, requirements, investor brief, FAQ.
- Paths: see Requirements/Integration Map at the end of this file.

Output Format (use for every task)
- Summary: 3–6 bullets with the decision and why.
- Recommendation: 1–2 paragraphs with the chosen option(s).
- Options & Trade-offs: concise table/list (quality, latency, CPU/GPU, footprint, license).
- Implementation Steps: file paths, env vars, code changes, and docs to edit; include effort (S/M/L) and owner.
- Bench Plan: dataset(s), metrics, target thresholds, and how to reproduce locally.
- Risks & Mitigations: top 3–5 with concrete mitigations.
- Sources: links with titles (papers, repos, docs, benchmarks).

Master Task Template (Ready to Paste)
Problem: <what to decide/improve> for Project Epoch (local-first personal AI).
Context: PoC uses JSONL store, `sentence-transformers/all-MiniLM-L6-v2`, FastAPI+Gradio, optional Ollama profile; bilingual docs exist; CPU viability required.
Constraints: offline-capable; consumer hardware; open/commercial-friendly licenses; zh/EN quality; CPU-first.
Output format: Summary; Recommendation; Options & trade-offs; Implementation steps (with repo file paths and env vars); Bench plan (datasets, metrics, targets); Risks; Sources.
Priority & Timebox: P0 (this week), 6–10 hours unless noted.

P0 Topics (High Priority)

1) Embeddings (EN/zh/multilingual) Selection — Ready Prompt
Research best local embeddings for a privacy-first, CPU-viable personal AI (Project Epoch). Compare MiniLM (`sentence-transformers/all-MiniLM-L6-v2`), `BAAI/bge-small-zh-v1.5`, and `BAAI/bge-m3` on quality (MTEB/BEIR including Chinese), CPU speed, memory footprint, and licenses. Output format as specified. Implementation should update `.env.example` (`EMBED_MODEL`), `docs/architecture*.md` guidance, and `docs/requirements*.md` defaults; include a fallback matrix by hardware tier.

2) Vector DB for Local-First — Ready Prompt
For a single-user local app, compare Chroma, Weaviate, and FAISS for persistence, offline ops, memory footprint, simplicity, and licensing. Recommend the first adapter to implement. Provide a storage interface design and a migration plan from JSONL. Include Compose/profile guidance. Update `docs/architecture*.md` and create an interface outline for `services/api` (no full code needed).

3) Retrieval Strategy Upgrade — Ready Prompt
Compare dense-only vs hybrid (BM25 + dense) vs MMR and cross-encoder rerankers (e.g., `bge-reranker-base/small`) with CPU viability. Recommend a staged retrieval pipeline for PoC and when-to-enable rules. Provide evaluation targets and thresholds. Update `docs/architecture*.md` accordingly.

4) Evaluation Baselines — Ready Prompt
Design a lightweight, reproducible local evaluation harness for latency (P50/P95) and retrieval quality (Recall@K/Hit@K) using small subsets from MTEB/BEIR and at least one Chinese corpus. Propose `scripts/eval_latency.py` and `scripts/eval_retrieval.py` outlines, datasets, metrics, and reporting. Update `docs/requirements*.md` with targets.

5) ASR Local Pipeline — Ready Prompt
Compare `faster-whisper` (small/base) and `whisper.cpp` for EN/zh accuracy, punctuation, diarization needs, and VAD (`silero-vad`). Provide CPU vs GPU trade-offs and default recommendations by hardware tier. Update `docs/requirements*.md` (defaults and sizing) and roadmap notes in `docs/architecture*.md`.

6) VLM for Image→Memory — Ready Prompt
Evaluate LLaVA 1.6 and Qwen2-VL (7B class) for caption/summary generation in EN/zh, VRAM needs, CPU feasibility, and licenses. Recommend a default and a fallback with constraints. Provide an API hook design for later integration. Update docs only.

7) Local LLM via Ollama — Ready Prompt
Compare `phi3:mini`, `mistral:7b-instruct`, and `qwen2:7b` for daily review/summarization latency and quality on consumer hardware. Discuss quantization choices. Provide recommended prompts. Update `README*` (“Try it”) and `docs/vision*.md` with suggested models.

8) Threat Model & Privacy Posture — Ready Prompt
Enumerate data-at-rest, logs, model downloads, and inter-service traffic risks. Propose encryption-at-rest options, least-privilege defaults, and minimal audit logging patterns that respect privacy. Add a “Security & Privacy” subsection to `docs/architecture*.md` and a short note to `docs/vision*.md`.

9) Licensing & Compliance — Ready Prompt
Produce a license matrix for BGE models, LLaVA, Qwen, Whisper variants, Chroma, and Weaviate, highlighting commercial-use constraints. Draft README disclaimers as needed. Output should include citations.

10) Data Schema & Portability — Ready Prompt
Refine the memory record schema (id/ts/source/modality/text/tags/embedding/meta), add export/import/versioning guidance, and propose migration notes from current JSONL. Update `docs/architecture*.md` and outline a future CLI.

11) Packaging for Offline Use — Ready Prompt
Outline model prefetching, Docker image layering, and a “no-network” compose profile. Provide instructions and risks. Update `README*` and `docs/requirements*.md` with offline steps.

12) KPI Targets & Guardrails — Ready Prompt
Propose realistic P0 targets per hardware tier (latency, retrieval quality, footprint). Add to `docs/requirements*.md` and the Metrics section in `docs/architecture*.md`.

P1 Topics (Backlog)

13) Hybrid Search for Chinese — Ready Prompt
Identify best BM25/tokenization for zh (jieba, pkuseg, character-level) and dense fusion strategy. Provide config notes and trade-offs.

14) Rerankers on CPU — Ready Prompt
Evaluate small cross-encoders (e.g., `bge-reranker-base/small`) for CPU throughput and quality. Recommend thresholds for when to enable rerank.

15) Streaming ASR & Diarization — Ready Prompt
Design a low-latency pipeline with VAD + partial hypotheses and simple diarization. Provide a staging plan and constraints.

16) Edge Hardware Playbooks — Ready Prompt
Benchmark Jetson Orin and Raspberry Pi (4/5) with recommended models. Provide an “Edge” appendix plan for `docs/requirements*.md`.

17) Observability (Privacy-Preserving) — Ready Prompt
Propose minimal local metrics/logging without telemetry, including redaction patterns and user controls. Update `docs/architecture*.md`.

18) Agent Tool Safety — Ready Prompt
Draft permissioning UX, dry-run diffs, and context limits for calendar/web actions. Provide policy and implementation guidance.

19) Model Routing Heuristics — Ready Prompt
Suggest rules/env design to route among small/large/remote models based on latency/cost/context size. Update docs and env.

20) Competitor Landscape — Ready Prompt
Compare Rewind, NotebookLM, AnythingLLM, Mem.dev, Personal.ai on privacy, ownership, offline capability, and openness. Provide a brief update for `docs/investor_brief*.md`.

21) Business Model Detail — Ready Prompt
Propose open-core packaging, paid add-ons, and pricing anchors. Update investor brief “Business Model/GTM”.

22) Community & Governance — Ready Prompt
Recommend best practices for CLA, Code of Conduct, Discussions structure, and contribution workflow. Provide doc templates to add.

Integration Map (Where to Apply Results)
- Requirements: `docs/requirements.md`, `docs/requirements.zh-CN.md`
- Architecture: `docs/architecture.md`, `docs/architecture.zh-CN.md`
- Vision/White Paper: `docs/vision*.md`, `WHITE_PAPER*.md`
- README: `README.md`, `README.zh-CN.md`
- Env/Compose: `.env.example`, `compose.yaml`
- API/Interfaces: `services/api/main.py`, (future) storage adapter module
- Evaluation scripts (to add): `scripts/eval_latency.py`, `scripts/eval_retrieval.py`

