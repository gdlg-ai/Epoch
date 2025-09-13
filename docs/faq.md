Frequently Asked Questions (FAQ)

Is my data private?
- Yes. Epoch is local-first. By default there are no external network calls. Optional remote models/services require explicit opt-in.

Does it work offline?
- Yes. After the first pull of Docker images/models, the stack runs offline.

Who owns my data?
- You do. Data is stored locally; export/import is part of the roadmap to make portability easy.

Do I need a GPU?
- No. The PoC runs on CPU. A GPU helps for faster ASR and local LLMs, but it’s optional.

What can I do today?
- Ingest short notes (text) and search by meaning (semantic search) via the local UI. Roadmap adds audio, images, and agent tools.

How is this different from cloud chatbots?
- Verifiable privacy (local-first), user-owned data, and a focus on memory and actions rather than chat alone.

What’s the license?
- Apache-2.0. You can use, modify, and build on it with attribution.

What’s the business model?
- Open-core. The core remains free and local; we may offer optional enterprise features, curated bundles, and partnerships.

Can I change models?
- Yes. Embedding/ASR/LLM/DB choices are or will be configurable via env vars and adapters. See `docs/architecture.md`.

Where are the system requirements?
- See `docs/requirements.md` for platform support and sizing tiers.

How do I contribute?
- Read `CONTRIBUTING.md`, browse open issues, and submit PRs. Feature requests and questions are welcome.

How do I remove my data?
- Stop the stack and delete the data directory mounted in `compose.yaml` (default `./data`). For future vector DBs, export/import tools will be provided.

