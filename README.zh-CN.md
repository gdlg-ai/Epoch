Project Epoch（开源 PoC）

英文版请见 `README.md`。

Project Epoch 是一个以隐私为核心的个人 AI 伴侣开源 PoC。目标是在本地完成最小闭环：捕获 → 转写 → 嵌入 → 存储 → 检索（RAG）→ 响应，并提供简洁可运行的 UI 与服务。

本仓库先行提供可运行的最小脚手架，便于快速迭代与透明协作。

快速开始
- 前置条件：Docker 与 Docker Compose（可选 GPU 驱动）
- 启动步骤：
  - 复制 `.env.example` 为 `.env`，按需调整
  - 运行：`docker compose up --build`
  - 打开 UI： http://localhost:7860

首批服务（第一轮）
- `api`（FastAPI）：基础记忆的写入/查询，简易 RAG 雏形
- `ui`（Gradio）：最小可用的录入与检索界面
- `ollama`（预置）：本地 LLM/VLM 运行环境（本轮默认不启用）

路线图（PoC）
- 阶段一（书记员）：音频→ASR→嵌入→向量库→文本 RAG；每日复盘
- 阶段二（图书管理员）：图像→VLM→记忆；多模型路由；深度 RAG
- 阶段三（贴身助理）：Agent 工具调用（日历/网页）；情景主动提醒

仓库结构
- `compose.yaml` — 容器编排
- `services/api` — FastAPI 后端（记忆写入/查询）
- `services/ui` — Gradio 前端
- `docs/` — 架构与白皮书（中英双语）

许可协议
Apache License 2.0，见 `LICENSE`。

参与贡献
- 参考 `docs/architecture.md` 与 issue 列表
- 欢迎 PR：ASR 流程、Embedding/向量库集成、RAG 提示词、VLM 接入、Agent 工具等

双语文档
- English：`README.md`、`docs/architecture.md`、`WHITE_PAPER.md`
- 中文：`README.zh-CN.md`、`docs/architecture.zh-CN.md`、`WHITE_PAPER.zh-CN.md`
