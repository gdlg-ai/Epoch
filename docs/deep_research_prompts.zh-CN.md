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

1）向量模型（英文/中文/多语）选择 —— 即贴即用
为隐私优先、CPU 可用的个人 AI（Project Epoch）调研最佳本地向量模型。比较 MiniLM（`sentence-transformers/all-MiniLM-L6-v2`）、`BAAI/bge-small-zh-v1.5`、`BAAI/bge-m3` 在质量（含中文 MTEB/BEIR）、CPU 速度、内存占用与许可。按“统一输出格式”产出。实施需更新 `.env.example`（`EMBED_MODEL`）、`docs/architecture*.md` 指南与 `docs/requirements*.md` 默认；按硬件档位给出回退矩阵。

2）本地优先向量库选择 —— 即贴即用
针对单用户本地应用，比较 Chroma、Weaviate、FAISS 的持久化、离线能力、内存占用、易用性与许可。推荐先实现的适配器。给出存储接口设计与从 JSONL 迁移计划；包含 Compose/profile 指引。更新 `docs/architecture*.md` 并在 `services/api` 提供接口草图（无需完整代码）。

3）检索策略升级 —— 即贴即用
比较纯向量 vs 混合（BM25 + 向量）vs MMR 与交叉编码重排（如 `bge-reranker-base/small`）的 CPU 可行性。给出 PoC 的分阶段检索管线与启用条件。提供评测目标与阈值。更新 `docs/architecture*.md`。

4）评测基线 —— 即贴即用
设计轻量、可复现的本地评测：延迟（P50/P95）与检索质量（Recall@K/Hit@K），采用 MTEB/BEIR 小子集与至少一个中文语料。提出 `scripts/eval_latency.py` 与 `scripts/eval_retrieval.py` 的脚本框架、数据集、指标与报告方式。更新 `docs/requirements*.md` 的目标值。

5）本地 ASR 流程 —— 即贴即用
比较 `faster-whisper`（small/base）与 `whisper.cpp` 在英文/中文准确率、断句、说话人分离需求与 VAD（`silero-vad`）。提供 CPU 与 GPU 的取舍与按硬件档位的默认推荐。更新 `docs/requirements*.md`（默认与容量分级）与 `docs/architecture*.md` 的路线图说明。

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

13）中文混合检索细节 —— 即贴即用
确定中文 BM25/分词（jieba、pkuseg、字粒度）与向量融合策略，提供配置建议与权衡。

14）CPU 上的重排器 —— 即贴即用
评估小型交叉编码器（如 `bge-reranker-base/small`）在 CPU 吞吐与质量，给出启用阈值建议。

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

