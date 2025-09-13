Vision (v0.2)

Vision
- A privacy-first, local-first “digital symbiont” that augments memory, provides proactive assistance, and executes tasks — owned and controlled by the individual.

Principles
- Privacy-first: local by default, minimal egress, auditable behavior.
- Open and portable: Apache-2.0, inspectable components, data export/import.
- Progressive: prove the minimal loop first; expand modalities/tools later.
- Minimal-yet-useful: ship the smallest cohesive experience.
- Composable: swappable ASR/Embeddings/DB/LLM via clean interfaces.
- Hardware-friendly: runnable on consumer PCs/RPi/Jetson.

User Value
- Memory augmentation: turn text/voice/images into a searchable personal KB.
- Instant recall: retrieve context, decisions, and traces when needed.
- Daily review: auto summaries/highlights/todos to drive reflection.
- Proactive help: contextual nudges to reduce slips and forgetfulness.
- Tool execution: integrate calendar/web/CLI to complete tasks (later).

Phases (aligned with repo roadmap)
- Chronicler: audio → ASR → embed → vector store → text RAG; daily digest.
- Librarian: VLM intake; model routing; deeper retrieval/re-ranking.
- Valet: agent tool-calls; scenario-based proactive reminders.

Non-Goals
- Cloud-first SaaS as the primary product form.
- “Do-everything” SOTA pursuit; we optimize for personal workflows.
- Social recommendation or ad-centric profiles.

Success Metrics
- Recall time: retrieve any key item from last 7 days within 1 minute.
- Retrieval quality: top-k hit rate and subjective relevance ≥ target (e.g., ≥80%).
- Local latency: end-to-end RAG P50 < 2s (relaxed for early PoC).
- Privacy: zero default data egress; auditable local-first behavior.
- Habit formation: weekly active usage and retention for review/search.

Differentiation
- Verifiable edge privacy and offline capability; user-owned, portable data.
- Open ecosystem: pluggable modules and tools; community-friendly design.
- Task-oriented: optimized for completing personal tasks, not generic chat.

Risks & Mitigations
- Edge performance: quantized/distilled models, async pipelines, optional accelerators.
- Retrieval quality: benchmarks + hard-case sets; re-ranking and routing iteration.
- Data security: local encryption, least privilege, revocation, “digital sabbath”.
- Over-reliance: visible controls and rate limiting; human-in-command defaults.

Near-Term Milestones
- v0.1 Daily Review Loop: ingest → embed → store → retrieve → summarize.
- Evaluation Baselines: small retrieval + latency benchmarks (scripted).
- Vector DB Migration: swap JSONL with Chroma/Weaviate behind an interface.
- Data Portability: export/import and one-shot index rebuild.

Learn More
- FAQ: `docs/faq.md`
