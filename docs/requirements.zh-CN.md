系统与硬件要求（v0.2 建议版）

摘要
- 本地优先 PoC 可在消费级硬件上通过 Docker 运行。GPU 可选；NVIDIA 将在 ASR/LLM 阶段显著加速。macOS 适合跑 UI/API（Docker）+ Ollama（宿主，Metal）。

支持平台
- Linux x86_64：Ubuntu 22.04 LTS（推荐）、Debian 12。
- macOS：13+（Intel 或 Apple Silicon）。Docker 内不支持 GPU 加速；使用 CPU 或宿主 Ollama。
- Windows 11：通过 WSL2（Ubuntu 22.04）。Docker Desktop 使用 WSL2 后端。
- 端侧：Raspberry Pi 4/5（ARM64）、NVIDIA Jetson（JetPack 5+）。性能有限，见分级建议。

软件前置
- Docker 24+ 与 Docker Compose v2。
- 可选 NVIDIA GPU（Linux）：驱动 535+、CUDA 12.x 运行时、`nvidia-container-toolkit`。
- 可选宿主 Python（非容器运行）：Python 3.10+，配合 `venv`/`pipx`。
- Ollama（可选 LLM/VLM）：使用最新版本；macOS 走 Metal，Linux 走 CUDA。

推荐默认（PoC）
- 向量模型（默认）：`BAAI/bge-small-zh-v1.5`（中文表现强，英文可用，CPU 友好）。可选：`BAAI/bge-small-en-v1.5`（偏英文）或 `BAAI/bge-m3`（多语 SOTA，较重）。
- ASR（阶段一后加入）：`faster-whisper` small/base；CPU 可用，GPU 适配更接近实时。
- VAD：`silero-vad`（轻量）。
- 向量存储：当前 JSONL；优先实现 ChromaDB 的适配器（嵌入式、Apache‑2.0），后续再考虑 Weaviate。
- LLM（经 Ollama，可选）：`phi3:mini`、`mistral:7b-instruct`、`qwen2:7b`。VLM：`llava:7b` 或后续 `qwen2-vl`。
- 检索：默认启用 MMR 重排（提升多样性）；规划混合检索（BM25 + 向量）。

- 环境变量（建议；部分为前瞻）
- `EMBED_MODEL`（默认：`BAAI/bge-small-zh-v1.5`）
- `ASR_MODEL`（默认：`faster-whisper-small`）
- `VECTOR_STORE`（默认：`jsonl`；后续：`chroma|weaviate`）
- `DEVICE`（默认：`cpu`；有 GPU 时为 `cuda`）
- `TOP_K`（默认：`5`）
- `USE_MMR`（默认：`true`）、`MMR_CANDIDATES`（默认：`20`）、`MMR_LAMBDA`（默认：`0.5`）

配置分级
- 最低 PoC（仅 CPU）：2 核、4 GB 内存、5 GB 磁盘。适合文本录入/检索与小体量记忆。
- 推荐开发机（CPU 或 NVIDIA）：8 核、16 GB 内存、20+ GB 磁盘。可选 8 GB 显存以提升 ASR/LLM。
- 工作站（NVIDIA）：12+ 核、32 GB 内存、24+ GB 显存以运行更大 LLM；优选 NVMe 磁盘。
- macOS（开发）：Apple Silicon M1/M2/M3，16 GB 内存。宿主跑 Ollama；API/UI 走 Docker。
- Raspberry Pi 4/5：4–8 GB 内存，建议外接 SSD。选用更小模型（MiniLM、whisper-small），批处理更稳。
- Jetson（边缘 GPU）：Orin Nano/AGX，JetPack 5+，8–16 GB 内存。可用 CUDA 版本的 Whisper/Embedding（视镜像而定）。

性能参考（近似）
- 向量（MiniLM/BGE-small）：CPU 下可满足交互式查询；大批量索引建议批处理。
- ASR（faster-whisper small）：现代 CPU 接近实时；中端 NVIDIA GPU 可达 2–4× 实时。
- 本地 RAG 端到端：推荐开发机目标 P50 < 2s；早期 PoC 可能更高，视模型与负载而定。

Docker 资源建议
- Docker Desktop（macOS/Windows）：分配 6+ CPU、8–12 GB 内存以获得流畅体验。
- NVIDIA（Linux）：安装 `nvidia-container-toolkit`；启用 GPU 服务时以 `--gpus all` 运行 compose。
- 离线：镜像/模型首次拉取后，可在离线环境运行。

安全与隐私
- 本地优先：默认无外联。启用远端模型前请检查 `.env` 与 compose 配置。
- 数据位置：通过 `MEMORY_PATH` 指定 JSONL；后续迁移到向量库并提供导入/导出。

后续迭代
- 提供常用 Embedding/ASR 的预构建镜像。
- 加入向量库适配器（Chroma/Weaviate）与迁移脚本。
- 发布延迟与检索准确度的评测脚本。
