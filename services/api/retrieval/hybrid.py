from typing import List, Tuple
from rank_bm25 import BM25Okapi
import jieba
import re
import numpy as np


def _is_chinese(s: str) -> bool:
    return sum('\u4e00' <= ch <= '\u9fff' for ch in s) > max(1, len(s) // 4)


def _tokenize(text: str) -> List[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if _is_chinese(text):
        return list(jieba.cut(text, cut_all=False))
    return text.lower().split()


class BM25Index:
    def __init__(self, corpus_texts: List[str], corpus_ids: List[str]):
        self.tokens = [_tokenize(t) for t in corpus_texts]
        self.ids = corpus_ids
        self._bm25 = BM25Okapi(self.tokens)

    def search(self, query: str, top_k: int = 5) -> List[Tuple[str, float]]:
        qtok = _tokenize(query)
        scores = self._bm25.get_scores(qtok)
        idx = np.argsort(scores)[::-1][:top_k]
        return [(self.ids[i], float(scores[i])) for i in idx if scores[i] > 0]


def mmr(query_vec: np.ndarray, doc_vecs: np.ndarray, top_k: int, lambda_mult: float = 0.7) -> List[int]:
    n = doc_vecs.shape[0]
    sim_to_query = (doc_vecs @ query_vec)  # (n,)
    selected: List[int] = []
    candidates = list(range(n))
    while len(selected) < min(top_k, n) and candidates:
        if not selected:
            best = int(np.argmax(sim_to_query[candidates]))
            selected.append(candidates.pop(best))
            continue
        remain = np.array([i for i in candidates], dtype=int)
        # similarity to already selected docs
        sim_sel = doc_vecs[remain] @ doc_vecs[selected].T  # (m, |S|)
        max_red = sim_sel.max(axis=1) if sim_sel.size else np.zeros(len(remain))
        mmr_score = lambda_mult * sim_to_query[remain] - (1 - lambda_mult) * max_red
        pick_idx = int(np.argmax(mmr_score))
        chosen = remain[pick_idx]
        selected.append(chosen)
        candidates.remove(chosen)
    return selected

