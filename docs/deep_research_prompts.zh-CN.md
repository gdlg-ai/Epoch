OpenAI Deep Research —— 题目包（Project Epoch v0.2）

全局指引（每个任务都先粘贴本段）
- 范围：隐私优先、本地优先；消费级硬件（CPU 为先，NVIDIA GPU 可选）；中英双语；开源与商用友好许可。
- 输出：执行摘要；推荐结论；选项与权衡矩阵；逐步实施方案；风险；基准（延迟/质量）；带 URL 的引用。
- 约束：可离线运行；优先小中型模型（≤ 8–13GB 显存）；必须支持 CPU 可用；许可需开源/商用友好。
- 交付物：可直接用于 PR 的文档更新、环境/配置默认值、接口设计概述、评测脚本方案。
- 验收：建议需映射到具体仓库文件，包含预估工作量与风险。

背景快照（当前仓库）
- PoC 闭环：录入（文本）→ 嵌入（MiniLM）→ JSONL 存储 → 余弦检索 → UI 响应。
- 后端/前端：FastAPI（`services/api`）、Gradio UI（`services/ui`）；Docker Compose，带可选 `ollama` profile。
- 向量模型：默认 `sentence-transformers/all-MiniLM-L6-v2`（`EMBED_MODEL` 可改）。
- API：`/health`；`/ingest`（可选 `ts`/`source`）；`/query`（返回 `ts`，支持 `TOP_K`）。
- 文档：双语愿景、架构、系统要求、投资摘要、FAQ 已就绪。

统一输出格式（每个任务都用）
- 摘要：3–6 条要点，说明结论与理由。
- 推荐：1–2 段，阐述最终选择与适用范围。
- 选项与权衡：列表/表格（质量、延迟、CPU/GPU、占用、许可）。
- 实施步骤：提交到哪些文件、需要的环境变量、代码/配置变更；标注工作量（S/M/L）与建议 owner。
- 评测方案：数据集、指标、目标阈值、本地复现方式。
- 风险与对策：3–5 条，给出具体缓解措施。
- 参考来源：论文、代码库、官方文档与基准链接。

主任务模板（即贴即用）
问题：为 Project Epoch（本地优先的个人 AI）决定/改进 <主题>。
上下文：PoC 使用 JSONL 存储、`all-MiniLM-L6-v2`、FastAPI+Gradio、可选 Ollama；已有双语文档；CPU 可用是硬约束。
约束：可离线；消费级硬件；开源/商用许可友好；中英文质量；CPU 为先。
输出格式：摘要；推荐；选项与权衡；实施步骤（含具体文件与环境变量）；评测方案（数据集、指标、目标）；风险；引用。
优先级与时间盒：P0（本周），6–10 小时（除非另述）。

P0 主题（高优先级）

已解决：向量模型选择 —— 默认采用 `BAAI/bge-small-zh-v1.5`；高阶可选 `BAAI/bge-m3`。

2）ChromaDB 适配器细化 —— 即贴即用
围绕单用户本地场景，细化 ChromaDB 的持久化选项（SQLite/DuckDB）、索引选择（HNSW/FAISS）、小数据量默认配置与备份/导出策略。输出：适配器设计要点；从 JSONL 的迁移步骤（id 映射、schema）；环境变量；可靠性建议。更新：`docs/architecture*.md`、`.env.example`，并给出 `services/api` 下的存储接口模块路径建议。

3）中文混合检索（BM25 + 向量） —— 即贴即用
选择适合 zh/EN 的 CPU 友好 BM25 实现（Whoosh vs Pyserini/Lucene），并确定中文分词/分析器（jieba/pkuseg/字粒度），以及与稠密向量的融合策略。输出：库选择、分析器配置、融合逻辑与阈值。更新：`docs/architecture*.md` 与系统要求。

已解决：评测脚本骨架已添加（`scripts/eval_latency.py`、`scripts/eval_retrieval.py`）。下一步：补充数据集选择与目标阈值。

已解决：默认 faster-whisper small + VAD；记录 base/量化与边缘设备回退。后续：分离（diarization）接入方案。

6）图像→记忆的 VLM 选择 —— 即贴即用
评估 LLaVA 1.6 与 Qwen2-VL（7B 量级）在中英文字幕/摘要的质量、显存需求、CPU 可行性与许可。推荐默认与回退方案及约束。提供后续接入的 API 钩子设计（仅文档）。

7）Ollama 本地 LLM —— 即贴即用
比较 `phi3:mini`、`mistral:7b-instruct`、`qwen2:7b` 在日常总结/每日复盘的延迟与质量（消费级硬件）。讨论量化方案。给出推荐提示词。更新 `README*` “2 分钟试用”与 `docs/vision*.md` 的模型建议。

8）威胁模型与隐私立场 —— 即贴即用
列举静态数据、日志、模型下载与服务间通信的风险，提出静态加密、最小权限默认与最小化审计日志的做法。为 `docs/architecture*.md` 增补“安全与隐私”，并在 `docs/vision*.md` 添加简短说明。

9）许可与合规 —— 即贴即用
给出 BGE、LLaVA、Qwen、Whisper 变体、Chroma、Weaviate 的许可矩阵，标注商用限制。草拟 README 所需的免责声明。必须附引用链接。

10）数据模式与可迁移性 —— 即贴即用
完善记录 schema（id/ts/source/modality/text/tags/embedding/meta），补充导入/导出/版本化与从 JSONL 的迁移说明。更新 `docs/architecture*.md` 并概述未来 CLI。

11）离线打包方案 —— 即贴即用
梳理模型预拉取、Docker 镜像分层与 “no-network” Compose profile 的步骤与风险。更新 `README*` 与 `docs/requirements*.md` 的离线操作说明。

12）KPI 目标与护栏 —— 即贴即用
按硬件档位提出现实的 P0 目标（延迟、检索质量、资源占用）。补充到 `docs/requirements*.md` 与 `docs/architecture*.md` 的指标章节。

P1 主题（后备清单）

已提升至 P0（见 #3）。

14）CPU 上的重排器 —— 即贴即用
评估 `bge-reranker-base/small` 在 CPU 的吞吐与质量，提出启用阈值与 `USE_RERANKER` 环境变量与默认建议。

15）流式 ASR 与分离 —— 即贴即用
设计低时延管线（VAD + 部分假设）与简易说话人分离，给出分阶段实施与约束。

16）边缘硬件手册 —— 即贴即用
对 Jetson Orin 与树莓派（4/5）做实测，产出推荐模型与参数，并规划 `docs/requirements*.md` 的“Edge”附录。

17）可观测性（隐私友好） —— 即贴即用
提出无遥测的本地化指标/日志方案，包含脱敏方式与用户可控项。更新 `docs/architecture*.md`。

18）Agent 工具安全 —— 即贴即用
起草权限 UX、干运行（diff）与上下文限额的策略与实现建议。

19）模型路由启发式 —— 即贴即用
给出在小/大/远端模型之间路由的规则与环境变量设计（基于延迟/成本/上下文）。更新文档与 env。

20）竞品概览 —— 即贴即用
比较 Rewind、NotebookLM、AnythingLLM、Mem.dev、Personal.ai 的隐私、数据所有权、离线能力与开放性，形成投资摘要的简报补充（`docs/investor_brief*.md`）。

21）商业模式细化 —— 即贴即用
提出开源内核的打包、付费增值项与价格锚点，更新投资摘要中的“商业模式/GTM”。

22）社区与治理 —— 即贴即用
推荐 CLA、行为准则（Code of Conduct）、Discussions 结构与贡献流程的最佳实践，并提供可直接添加的文档模板。

整合路径（结果应用位置）
- 系统要求：`docs/requirements.md`、`docs/requirements.zh-CN.md`
- 架构：`docs/architecture.md`、`docs/architecture.zh-CN.md`
- 愿景/白皮书：`docs/vision*.md`、`WHITE_PAPER*.md`
- 首页 README：`README.md`、`README.zh-CN.md`
- 环境/编排：`.env.example`、`compose.yaml`
- API/接口：`services/api/main.py`，以及未来的存储适配器模块
- 评测脚本（待新增）：`scripts/eval_latency.py`、`scripts/eval_retrieval.py`
