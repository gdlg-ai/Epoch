System Requirements and Recommended Configs (v0.2)

Summary
- Local-first PoC runs on consumer hardware with Docker. GPU is optional; NVIDIA accelerates ASR/LLM later phases. macOS works well for UI/API and Ollama (outside Docker) with Metal.

Supported Platforms
- Linux x86_64: Ubuntu 22.04 LTS (recommended), Debian 12.
- macOS: 13+ (Intel or Apple Silicon). GPU accel in Docker is not available; use CPU or Ollama on host.
- Windows 11: via WSL2 (Ubuntu 22.04). Run Docker Desktop with WSL2 backend.
- Edge: Raspberry Pi 4/5 (ARM64), NVIDIA Jetson (JetPack 5+). Performance is modest; see tiers below.

Software Prerequisites
- Docker 24+ and Docker Compose v2.
- Optional NVIDIA GPU (Linux): driver 535+ and CUDA 12.x runtime, plus `nvidia-container-toolkit`.
- Optional host Python (non-Docker runs): Python 3.10+ and `pipx`/`venv`.
- Ollama (optional LLM/VLM): latest release; Metal on macOS, CUDA on Linux.

Recommended Defaults (PoC)
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2` (English) OR `BAAI/bge-small-zh-v1.5` (Chinese) OR `BAAI/bge-m3` (multilingual).
- ASR (optional in Phase 1+): `faster-whisper` small/base; CPU okay, GPU preferred for real-time.
- VAD: `silero-vad` (lightweight).
- Vector store: JSONL (current PoC); plan to switch to Chroma or Weaviate behind a storage interface.
- LLM (via Ollama, optional): `phi3:mini`, `mistral:7b-instruct`, `qwen2:7b`. VLM: `llava:7b` or `qwen2-vl` later.

Env Vars (suggested; some may be future-facing)
- `EMBED_MODEL` (default: `sentence-transformers/all-MiniLM-L6-v2`)
- `ASR_MODEL` (default: `faster-whisper-small`)
- `VECTOR_STORE` (default: `jsonl`; future: `chroma|weaviate`)
- `DEVICE` (default: `cpu`; future: `cuda` when available)
- `TOP_K` (default: `5`)

Sizing Tiers
- Minimum PoC (CPU-only): 2 cores, 4 GB RAM, 5 GB free disk. Suitable for text ingest/query and small memories.
- Recommended Dev (CPU or NVIDIA GPU): 8 cores, 16 GB RAM, 20+ GB disk. Optional GPU (8 GB VRAM) improves ASR/LLM.
- Workstation (NVIDIA): 12+ cores, 32 GB RAM, 24+ GB VRAM for larger LLMs; fast disks (NVMe).
- macOS (Dev): Apple Silicon M1/M2/M3, 16 GB RAM. Use Ollama on host for LLM; run API/UI in Docker.
- Raspberry Pi 4/5: 4–8 GB RAM, prefer SSD over SD. Use smaller models (MiniLM, whisper-small) and batch jobs.
- Jetson (Edge GPU): Orin Nano/AGX, JetPack 5+, 8–16 GB RAM. Use CUDA builds of Whisper and embeddings when available.

Performance Guidelines (approximate)
- Embeddings (MiniLM/BGE-small): responsive on CPU for interactive queries; batch indexing recommended for large corpora.
- ASR (faster-whisper small): CPU approaches real-time on modern CPUs; 2–4× real-time on mid-range NVIDIA GPUs.
- RAG end-to-end (local): target P50 < 2s on Recommended Dev; initial PoC may be higher depending on models.

Docker Resource Tips
- Docker Desktop (macOS/Windows): allocate 6+ CPUs and 8–12 GB RAM for smooth development.
- NVIDIA (Linux): install `nvidia-container-toolkit`; run compose with `--gpus all` if enabling GPU services.
- Air-gap: after images/models are pulled once, the stack can run offline.

Security & Privacy
- Local-first: no external calls by default. Verify `.env` and compose profiles before enabling remote models.
- Data location: memory JSONL path via `MEMORY_PATH` (see `.env.example`). Plan migration to vector DB with export/import.

Next Iterations
- Provide prebuilt model images for common embeddings/ASR.
- Add vector DB adapters (Chroma/Weaviate) and migration script.
- Publish evaluation scripts for latency and retrieval accuracy.

