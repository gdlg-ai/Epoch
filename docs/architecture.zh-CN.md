架构说明（PoC 第一轮）

范围：在本地完成最小可行的“记忆闭环”，并提供简洁 UI。

分层
- 捕获：本轮以手动文本录入为起点（后续补音频/视觉）
- 记忆：JSONL 存储 + Embedding（sentence-transformers）+ 余弦相似检索
- 认知：占位（后续通过 Ollama 对接本地 LLM）
- 交互：FastAPI 后端 + Gradio 前端

数据流
- /ingest：文本（+标签）→ 追加写入 JSONL → 生成向量 → 内存索引
- /query：问题 → 生成向量 → 余弦相似 → 候选集 → 可选 MMR 重排 → Top-K 结果

服务
- api：FastAPI，提供 `/health`、`/ingest`、`/query`
- ui：Gradio，调用上述 API
- ollama：预留，当前默认关闭（按需在 compose 开启）

下一步
- 将 JSONL 替换为向量数据库（优先 ChromaDB 适配器；后续再考虑 Weaviate）
- 引入 ASR（Whisper/faster-whisper）与 VAD
- 整合 VLM（如 LLaVA/Qwen-VL）实现图像→文本入库
- 引入本地 LLM + RAG 的推理层
- 增加模型路由与 Agent 工具调用

双语文档
- 英文版：`docs/architecture.md`

设计准则
- 隐私优先：本地默认、外发最小且需显式配置。
- 可组装：ASR/Embedding/DB/LLM 可替换，接口清晰。
- 极简可用：偏向简单、可观测的管线而非复杂度。

数据模型（PoC）
- 记录：`id`（uuid）、`ts`（ISO）、`source`（如 ui/api）、`modality`（text|audio|image）、`text`、`tags`（string[]）、`embedding`（float[]）、`meta`（可选对象）。
- 存储：运行期 JSONL（追加式）。规划：在存储接口下切换向量库实现。

API 契约（当前）
- `GET /health` → `{"status":"ok"}`
- `POST /ingest` 请求体：`{ text: string, tags?: string[], source?: string, ts?: string }` → 响应：`{ id: string }`
- `POST /query` 请求体：`{ query: string, top_k?: number }` → 响应：`{ results: [{ id, text, tags, ts, score }] }`

配置
- 向量模型：环境变量（如 `EMBED_MODEL=sentence-transformers/all-MiniLM-L6-v2`）。
- 设备/运行：默认 CPU，可选 GPU。
- 存储类型：PoC 为 JSONL；后续 `VECTOR_STORE=chroma|weaviate`。

运维
- 本地运行：`docker compose up --build` → 打开 `http://localhost:7860`。
- 数据位置：PoC JSONL 位于 api 服务的数据目录（实现细节，向量库后可能调整）。
- 导入/导出：规划中；随向量库加入索引重建命令。

指标与基准（目标）
- 本地 RAG 端到端 P50 < 2s（早期可放宽）。
- 检索质量：Top‑K 命中率/主观相关性 ≥ 80% 目标。
- 资源占用：在消费级硬件无独显也可运行。

检索策略
- 基线：稠密向量 + 余弦相似。
- 多样性：对候选结果启用 MMR 重排。
- 混合（规划）：加入 BM25 词法检索（Whoosh/Pyserini）并与向量结果融合。

迁移计划（向量数据库）
- 步骤一：引入存储接口；保留 JSONL 适配器。
- 步骤二：加入 ChromaDB 适配器；对齐测试；迁移脚本。
- 步骤三：可选 Weaviate 适配器；通过配置切换。

安全与隐私
- 本地优先默认；除非显式配置，否则无网络外发。
- 可审计：本地记录最小化的 ingest/query 事件日志。

相关文档
- 愿景：`docs/vision.zh-CN.md`

硬件档位（速览）
- 最低 PoC（仅 CPU）：2 核、4 GB 内存 —— 文本录入/检索。
- 推荐开发机：8 核、16 GB 内存 —— 端到端 P50 目标 < 2s。
- 工作站（GPU）：12+ 核、32 GB 内存、≥8–24 GB 显存以运行更大 LLM。
- macOS：Docker 跑 API/UI；宿主用 Ollama 跑 LLM。
