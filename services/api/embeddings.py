import os
from typing import List
from sentence_transformers import SentenceTransformer


_BGE_PREFIX_ZH = os.getenv("EMBED_QUERY_PREFIX_ZH", "为这个句子生成表示以用于检索相关文章：")
_BGE_PREFIX_EN = os.getenv("EMBED_QUERY_PREFIX_EN", "Represent this sentence for retrieving related passages:")
_ADD_PREFIX = os.getenv("EMBED_ADD_QUERY_PREFIX", "true").lower() == "true"


class EmbeddingModel:
    def __init__(self):
        model_name = os.getenv("EMBED_MODEL", "BAAI/bge-small-zh-v1.5")
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self._is_bge = model_name.lower().startswith("baai/bge")

    def _add_query_prefix(self, text: str) -> str:
        if not _ADD_PREFIX or not self._is_bge:
            return text
        zh_chars = sum('\u4e00' <= ch <= '\u9fff' for ch in text)
        zh = zh_chars > max(1, len(text) // 4)
        return f"{_BGE_PREFIX_ZH if zh else _BGE_PREFIX_EN}{text}"

    def embed_docs(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, normalize_embeddings=True).tolist()

    def embed_query(self, text: str) -> List[float]:
        return self.model.encode([self._add_query_prefix(text)], normalize_embeddings=True)[0].tolist()

