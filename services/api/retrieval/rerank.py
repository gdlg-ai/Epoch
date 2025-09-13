import os
from typing import List


class CrossEncoderReranker:
    def __init__(self):
        self.name = os.getenv("RERANKER_MODEL", "BAAI/bge-reranker-base")
        self._model = None
        self._tokenizer = None
        self._device = None

    def _lazy(self):
        if self._model is not None:
            return
        try:
            import torch
            from transformers import AutoTokenizer, AutoModelForSequenceClassification
        except Exception as e:
            raise RuntimeError(
                "Transformers/torch not installed. Install to enable reranker."
            ) from e
        self._device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )
        self._tokenizer = AutoTokenizer.from_pretrained(self.name)
        self._model = AutoModelForSequenceClassification.from_pretrained(self.name).to(
            self._device
        )

    def score(self, query: str, passages: List[str]) -> List[float]:
        self._lazy()
        from transformers import AutoTokenizer  # type: ignore
        import torch  # type: ignore

        pairs = [(query, p) for p in passages]
        toks = self._tokenizer(
            pairs,
            padding=True,
            truncation=True,
            return_tensors="pt",
            max_length=512,
        )
        toks = {k: v.to(self._device) for k, v in toks.items()}
        with torch.no_grad():
            logits = self._model(**toks).logits.squeeze(-1)
        return logits.detach().cpu().tolist()

