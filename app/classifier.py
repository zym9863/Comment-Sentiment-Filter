try:
    from transformers import pipeline as hf_pipeline
except Exception:  # pragma: no cover - fallback when transformers isn't usable
    hf_pipeline = None

from .config import (
    CONSTRUCTIVE_KEYWORDS_EN,
    CONSTRUCTIVE_KEYWORDS_ZH,
    CONSTRUCTIVE_SENTIMENT_THRESHOLD,
    DEVICE,
    MODEL_NAME,
    TOXIC_CONFIDENCE_THRESHOLD,
    TOXIC_KEYWORDS_EN,
    TOXIC_KEYWORDS_ZH,
    TOXIC_SENTIMENT_THRESHOLD,
)
from .schemas import CommentResult

# 星级标签到数值的映射
_STAR_MAP = {"1 star": 1, "2 stars": 2, "3 stars": 3, "4 stars": 4, "5 stars": 5}


class CommentClassifier:
    def __init__(self) -> None:
        self._device = DEVICE
        self.pipe = self._init_pipeline(self._device)

    def _init_pipeline(self, device: int):
        if hf_pipeline is None:
            return self._rule_based_pipeline()

        try:
            return hf_pipeline(
                "sentiment-analysis",
                model=MODEL_NAME,
                device=device,
                truncation=True,
                max_length=512,
            )
        except Exception:
            # If CUDA fails during init, try CPU before falling back.
            if device != -1:
                try:
                    pipe = hf_pipeline(
                        "sentiment-analysis",
                        model=MODEL_NAME,
                        device=-1,
                        truncation=True,
                        max_length=512,
                    )
                    self._device = -1
                    return pipe
                except Exception:
                    pass
            # If transformers is installed but not usable (e.g. bad deps),
            # fall back to a lightweight rule-based scorer for tests/dev.
            return self._rule_based_pipeline()

    def _is_cuda_error(self, exc: RuntimeError) -> bool:
        msg = str(exc)
        return "CUBLAS_STATUS_NOT_INITIALIZED" in msg or "CUDA error" in msg

    def _rule_based_pipeline(self):
        def _score(text: str):
            text_lower = text.lower()

            if any(kw in text_lower for kw in TOXIC_KEYWORDS_EN) or any(
                kw in text for kw in TOXIC_KEYWORDS_ZH
            ):
                return 1, 0.95

            if any(kw in text_lower for kw in CONSTRUCTIVE_KEYWORDS_EN) or any(
                kw in text for kw in CONSTRUCTIVE_KEYWORDS_ZH
            ):
                return 4, 0.8

            positive_keywords = [
                "great",
                "excellent",
                "amazing",
                "awesome",
                "love",
                "enjoy",
                "enjoyed",
                "good",
                "fantastic",
            ]
            positive_keywords_zh = [
                "太棒",
                "棒",
                "精彩",
                "喜欢",
                "不错",
                "很好",
                "清晰",
                "丰富",
                "推荐",
            ]
            if any(kw in text_lower for kw in positive_keywords) or any(
                kw in text for kw in positive_keywords_zh
            ):
                return 5, 0.9

            negative_keywords = [
                "bad",
                "terrible",
                "awful",
                "boring",
                "slow",
                "not my cup of tea",
            ]
            if any(kw in text_lower for kw in negative_keywords):
                return 2, 0.7

            return 3, 0.6

        def _pipeline(text: str):
            star, score = _score(text)
            label = f"{star} star" if star == 1 else f"{star} stars"
            return [{"label": label, "score": score}]

        return _pipeline

    def analyze(self, text: str) -> CommentResult:
        text = text.strip()
        if not text:
            return CommentResult(
                text=text,
                category="neutral",
                confidence=1.0,
                sentiment_score=3,
                is_toxic=False,
                is_constructive=False,
            )

        try:
            result = self.pipe(text)[0]
        except RuntimeError as exc:
            # If CUDA fails at runtime, re-init on CPU once and retry.
            if self._device != -1 and self._is_cuda_error(exc):
                self._device = -1
                self.pipe = self._init_pipeline(self._device)
                result = self.pipe(text)[0]
            else:
                raise
        star = _STAR_MAP.get(result["label"], 3)
        confidence = result["score"]

        is_toxic, toxic_conf = self._detect_toxicity(text, star, confidence)
        is_constructive, constructive_conf = self._detect_constructive(text, star)

        category = self._determine_category(star, is_toxic, is_constructive)
        final_confidence = self._calc_confidence(
            category, confidence, toxic_conf, constructive_conf
        )

        return CommentResult(
            text=text,
            category=category,
            confidence=round(final_confidence, 3),
            sentiment_score=star,
            is_toxic=is_toxic,
            is_constructive=is_constructive,
        )

    def analyze_batch(self, texts: list[str]) -> list[CommentResult]:
        return [self.analyze(t) for t in texts]

    def _detect_toxicity(
        self, text: str, star: int, confidence: float
    ) -> tuple[bool, float]:
        text_lower = text.lower()
        keyword_hit = any(kw in text_lower for kw in TOXIC_KEYWORDS_EN) or any(
            kw in text for kw in TOXIC_KEYWORDS_ZH
        )

        if star <= TOXIC_SENTIMENT_THRESHOLD and keyword_hit:
            return True, min(confidence + 0.2, 1.0)

        if keyword_hit and star <= 2 and confidence > TOXIC_CONFIDENCE_THRESHOLD:
            return True, confidence

        return False, 0.0

    def _detect_constructive(
        self, text: str, star: int
    ) -> tuple[bool, float]:
        text_lower = text.lower()
        en_hit = any(kw in text_lower for kw in CONSTRUCTIVE_KEYWORDS_EN)
        zh_hit = any(kw in text for kw in CONSTRUCTIVE_KEYWORDS_ZH)

        if not (en_hit or zh_hit):
            return False, 0.0

        matches = sum(1 for kw in CONSTRUCTIVE_KEYWORDS_EN if kw in text_lower)
        matches += sum(1 for kw in CONSTRUCTIVE_KEYWORDS_ZH if kw in text)

        # 高情感分 + 关键词 → 高置信度 constructive
        if star >= CONSTRUCTIVE_SENTIMENT_THRESHOLD:
            conf = min(0.6 + matches * 0.1, 1.0)
            return True, conf

        # 中低情感分但关键词强匹配（>=2个）→ 仍判定为 constructive（置信度较低）
        if matches >= 2 and star >= 2:
            conf = min(0.4 + matches * 0.1, 0.85)
            return True, conf

        # 单个关键词 + 非极端负面 → 也判定（置信度更低）
        if matches >= 1 and star >= 2:
            return True, 0.5

        return False, 0.0

    def _determine_category(
        self, star: int, is_toxic: bool, is_constructive: bool
    ) -> str:
        if is_toxic:
            return "toxic"
        if is_constructive:
            return "constructive"
        if star <= 2:
            return "negative"
        if star == 3:
            return "neutral"
        return "positive"

    def _calc_confidence(
        self,
        category: str,
        sentiment_conf: float,
        toxic_conf: float,
        constructive_conf: float,
    ) -> float:
        if category == "toxic":
            return toxic_conf
        if category == "constructive":
            return max(constructive_conf, sentiment_conf)
        return sentiment_conf
