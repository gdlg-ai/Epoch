Project Epoch — 开源 PoC 白皮书（v0.2 精要）

愿景
- 从被动助手迈向“数字共生体”：以隐私为先，具备终身记忆、主动协助与任务执行能力的个人 AI。

原则
- 隐私优先（默认本地）、完全开源（Apache-2.0）、硬件无关（PoC 阶段）、社区共建。

PoC 目标（更新）
- 打通个人记忆闭环（文本先行；已加入音频；视觉随后）
- 在本地以嵌入式向量库（Chroma）实现基于个人记忆的 RAG
- 初步多模态路径（图→文→入库）
- 可在消费级硬件（PC/RPi/Jetson）上运行

技术选型（v0.2）
- ASR：faster-whisper（small/base，本地，含 VAD）
- Embedding：BGE-small-zh（默认，CPU 友好），BGE-M3（可选，建议 GPU）
- 向量存储：ChromaDB（嵌入式、持久化、离线）默认；JSONL 作为回退
- LLM/VLM：通过 Ollama（Phi-3、Mistral、LLaVA/Qwen-VL）
- 后端：FastAPI；前端：Gradio；编排：Docker Compose

路线图
- 阶段一（书记员）：记忆流程 + 向量库 + 每日复盘；建立评测基线
- 阶段二（图书管理员）：VLM 入库；模型路由；混合检索与重排
- 阶段三（贴身助理）：Agent 工具调用；情景化主动提醒

伦理
- 明确授权、流程透明、本地可控，并提供“数字安息日”等避免过度依赖的选项。

本 PoC 仅是起点，期待社区共同参与，把愿景落为开放生态。

附录
- 常见问题（FAQ）：`docs/faq.zh-CN.md`
