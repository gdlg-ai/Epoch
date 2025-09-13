Contributing to Project Epoch

Thanks for your interest in contributing! This project aims to be a privacy-first, local-first personal AI. We value simplicity, openness, and user trust.

Ways to contribute
- Features: ASR pipeline, embeddings/vector DB adapters, RAG prompts, VLM intake, agent tools.
- Quality: evaluation scripts (latency/retrieval), docs, examples, DX improvements.
- Issues: bug reports and feature requests using the templates in `.github/ISSUE_TEMPLATE`.

Development setup
- Prereqs: Docker 24+ and Compose v2. Optional NVIDIA GPU on Linux.
- Run: `docker compose up --build` and open `http://localhost:7860`.

Code guidelines
- Keep changes minimal and focused; prefer composable interfaces.
- Avoid hard-coding model/store choices; read from env when possible.
- Add or update docs when behavior changes.

Storage interface roadmap
- Current: JSONL append-only store inside `api` service.
- Next: introduce a storage interface, add Chroma adapter, then Weaviate.

Pull requests
- Start with an issue for larger changes.
- Include usage notes and any migration or config changes.
- Ensure lint/format and basic runtime sanity locally before PR.

Community and governance
- We use GitHub Issues/PRs and Discussions (once enabled) for coordination.
- Be respectful and constructive. Privacy and openness are non-negotiable values here.

