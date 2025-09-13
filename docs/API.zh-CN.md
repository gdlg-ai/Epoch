API 参考（v0.2）

基础地址
- 默认：`http://localhost:8000`

接口
- `GET /health`
  - 返回：`{ "status": "ok", "items": number }`

- `GET /model`
  - 返回：当前嵌入/检索/存储/ASR 的配置摘要，例如：
    ```json
    {
      "embedding": {"model": "BAAI/bge-small-zh-v1.5", "add_query_prefix": "true"},
      "retrieval": {"top_k": 5, "use_mmr": true, "enable_bm25": true, "enable_reranker": false},
      "storage": {"backend": "chroma", "chroma_persist_dir": "/app/data/chroma"},
      "asr": {"enabled": "true", "size": "small", "device": "auto"}
    }
    ```

- `POST /ingest`
  - JSON 请求体：`{ text: string, tags?: string[], source?: string, ts?: string }`
  - 返回：`{ ok: boolean, id?: string }`
  - 说明：默认向量库为 Chroma，会生成内部 `id` 并持久化。

- `POST /query`
  - JSON 请求体：`{ query: string, top_k?: number }`
  - 返回：`{ results: [{ text: string, tags: string[], ts?: string, score: number }] }`
  - 说明：默认开启 MMR 多样化。BM25/混合检索与重排器可通过环境变量开关。

- `POST /asr`
  - 表单：`file=<audio>`
  - 返回：`{ language: string, text: string, segments: [{ start: number, end: number, text: string }] }`
  - 说明：当 `ASR_ENABLED=true` 时启用，基于 faster-whisper small/base 本地运行。

环境开关（部分）
- 检索：`TOP_K`、`USE_MMR`、`ENABLE_BM25`、`ENABLE_RERANKER`
- 向量：`EMBED_MODEL`、`EMBED_ADD_QUERY_PREFIX`
- 存储：`VECTOR_STORE=chroma|jsonl`、`CHROMA_PERSIST_DIR`
