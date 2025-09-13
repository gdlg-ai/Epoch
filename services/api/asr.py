import os
from typing import Any, Dict


class ASR:
    def __init__(self):
        self._model = None

    def _lazy(self):
        if self._model is not None:
            return
        try:
            from faster_whisper import WhisperModel  # type: ignore
        except Exception as e:
            raise RuntimeError(
                "faster-whisper not installed. Install to enable ASR."
            ) from e
        size = os.getenv("ASR_MODEL_SIZE", "small")
        dev_opt = os.getenv("ASR_DEVICE", "auto")
        device = (
            "cuda"
            if (dev_opt == "cuda")
            else ("cuda" if dev_opt == "auto" and self._cuda_available() else "cpu")
        )
        compute_type = "float16" if device == "cuda" else "int8"
        self._model = WhisperModel(size, device=device, compute_type=compute_type)

    def _cuda_available(self) -> bool:
        try:
            import torch  # type: ignore

            return torch.cuda.is_available()
        except Exception:
            return False

    def transcribe(self, audio_path: str, vad: bool = True) -> Dict[str, Any]:
        self._lazy()
        from faster_whisper import WhisperModel  # type: ignore

        segments, info = self._model.transcribe(
            audio_path, vad_filter=vad, beam_size=5
        )
        texts, segs = [], []
        for s in segments:
            segs.append({"start": float(s.start), "end": float(s.end), "text": s.text})
            texts.append(s.text.strip())
        return {
            "language": getattr(info, "language", "unk"),
            "text": " ".join(texts).strip(),
            "segments": segs,
        }

