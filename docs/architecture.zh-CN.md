架构说明（PoC 第一轮）

范围：在本地完成最小可行的“记忆闭环”，并提供简洁 UI。

分层
- 捕获：本轮以手动文本录入为起点（后续补音频/视觉）
- 记忆：JSONL 存储 + Embedding（sentence-transformers）+ 余弦相似检索
- 认知：占位（后续通过 Ollama 对接本地 LLM）
- 交互：FastAPI 后端 + Gradio 前端

数据流
- /ingest：文本（+标签）→ 追加写入 JSONL → 生成向量 → 内存索引
- /query：问题 → 生成向量 → 余弦相似 → Top-K 结果

服务
- api：FastAPI，提供 `/health`、`/ingest`、`/query`
- ui：Gradio，调用上述 API
- ollama：预留，当前默认关闭（按需在 compose 开启）

下一步
- 将 JSONL 替换为向量数据库（ChromaDB/Weaviate）
- 引入 ASR（Whisper/faster-whisper）与 VAD
- 整合 VLM（如 LLaVA/Qwen-VL）实现图像→文本入库
- 引入本地 LLM + RAG 的推理层
- 增加模型路由与 Agent 工具调用

双语文档
- 英文版：`docs/architecture.md`
