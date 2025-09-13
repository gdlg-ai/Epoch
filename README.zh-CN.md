Project Epoch —— 私有、可信赖的个人 AI（开源）

English: see `README.md`。

Epoch 致力于成为“你的数字共生体”：隐私优先、默认本地，帮你记忆、主动协助、并能执行任务——数据完全由你掌控。当前是最小可运行 PoC；愿景是把一个可验证、可迁移的个人 AI 带到每个人的设备上。

为什么重要
- 可验证的隐私：默认本地，无意外外发。
- 你的第二大脑：随时找回对话、笔记与图片要点。
- 从聊天到行动：从问答升级为真正完成任务。
- 开放可迁移：Apache‑2.0，数据可导入/导出，社区共建。

2 分钟试用
- 前置条件：Docker 与 Docker Compose（可选 GPU 驱动）
- 启动步骤：
  - 复制 `.env.example` 为 `.env`，按需调整
  - 运行：`docker compose up --build`
  - 打开 UI： http://localhost:7860

你现在能做什么
- 录入短笔记（文本），立即按语义检索（相似度搜索）。
- 体验最小 UI 与 API，全部在本机运行。
- 透明了解“嵌入—存储—检索”的工作方式。
- 默认使用 `BAAI/bge-small-zh-v1.5` 作为向量模型（中英皆佳，CPU 友好）；可通过 `EMBED_MODEL` 切换。
 - 存储默认使用嵌入式向量库 Chroma（本地持久化）；可通过 `VECTOR_STORE` 切换。

路线图
- 阶段一 —— 书记员：音频→ASR→嵌入→向量库→文本 RAG；每日复盘
- 阶段二 —— 图书管理员：图像→VLM→记忆；模型路由；更深检索/重排
- 阶段三 —— 贴身助理：Agent 工具调用（日历/网页）；情景化主动提醒

如何构建（一眼看懂）
- `compose.yaml` — 容器编排
- `services/api` — FastAPI 后端（记忆写入/查询）
- `services/ui` — Gradio 前端
- `docs/` — 架构与白皮书（中英双语）
 - 系统与硬件要求见：`docs/requirements.zh-CN.md`

愿景与架构
- 愿景：`docs/vision.zh-CN.md`（英文版：`docs/vision.md`）
- 架构：`docs/architecture.zh-CN.md`（英文版：`docs/architecture.md`）
 - 投资摘要：`docs/investor_brief.zh-CN.md`（英文版：`docs/investor_brief.md`）
 - 深度研究题目包：`docs/deep_research_prompts.zh-CN.md`（英文版：`docs/deep_research_prompts.md`）
 - API 参考：`docs/API.zh-CN.md`（英文版：`docs/API.md`）

里程碑
- v0.1 —— 每日复盘闭环（录入→嵌入→存储→检索→总结）
- 下一步 —— 检索/延迟评测基线；在接口抽象下完成向量库迁移

适用人群
- 想要“真正属于自己”的第二大脑的个人用户。
- 对隐私敏感的团队（法务、医疗、研发）需要本地优先 AI。
- 偏好开放、可替换组件而非封闭黑盒的建设者。

支持项目
- 试用 PoC，并在 issues 中反馈体验与需求。
- Star 仓库，帮助提升可见度与社区参与。
- 通过 PR 贡献模块（ASR/Embedding/向量库/LLM 工具）。
- 欢迎合作与投资洽谈：我们正在将“可信个人 AI”的蓝图从 PoC 落地为可规模化的产品与生态。

许可协议
Apache License 2.0，见 `LICENSE`。

参与贡献
- 参考 `docs/architecture.md` 与 issue 列表
- 欢迎 PR：ASR 流程、Embedding/向量库集成、RAG 提示词、VLM 接入、Agent 工具等

本地基准测试
- 延迟：`python scripts/eval_latency.py --host http://localhost:8000`
- 检索（玩具集 Recall@K）：`python scripts/eval_retrieval.py --host http://localhost:8000`

常见问题（FAQ）
- 我的数据安全吗？安全。默认本地运行，除非你主动开启外联。
- 能离线用吗？能。镜像/模型首次拉取后即可离线运行。
- 一定要有 GPU 吗？不需要。PoC 下 CPU 足够；GPU 主要用于 ASR/LLM 加速。
- 与云端聊天机器人有何不同？数据归你所有；可验证“本地优先”；我们专注于“记忆 + 行动”。
- 商业模式？开源内核 + 企业增值与生态合作。
 - 完整 FAQ：`docs/faq.zh-CN.md`

双语文档
- English：`README.md`、`docs/architecture.md`、`WHITE_PAPER.md`
- 中文：`README.zh-CN.md`、`docs/architecture.zh-CN.md`、`WHITE_PAPER.zh-CN.md`
 - 系统要求：`docs/requirements.md`（中文：`docs/requirements.zh-CN.md`）
