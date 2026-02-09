"""分类器单元测试。

注意：首次运行需要下载 BERT 模型（~700MB），请确保网络通畅。
"""

import pytest

from app.classifier import CommentClassifier


@pytest.fixture(scope="module")
def classifier():
    return CommentClassifier()


class TestClassifierCategories:
    """测试各分类是否能正确识别。"""

    def test_toxic_chinese(self, classifier):
        result = classifier.analyze("你这个白痴，做的什么垃圾东西！")
        assert result.is_toxic is True
        assert result.category == "toxic"

    def test_toxic_english(self, classifier):
        result = classifier.analyze("You're such an idiot, this is absolute trash!")
        assert result.is_toxic is True
        assert result.category == "toxic"

    def test_negative_chinese(self, classifier):
        result = classifier.analyze("这个视频有点无聊，感觉没什么新意。")
        assert result.category in ("negative", "neutral")
        assert result.is_toxic is False

    def test_negative_english(self, classifier):
        result = classifier.analyze("Not my cup of tea. The pacing was too slow.")
        assert result.category in ("negative", "neutral")
        assert result.is_toxic is False

    def test_positive_chinese(self, classifier):
        result = classifier.analyze("这个视频太棒了！内容丰富，讲解清晰！")
        assert result.category in ("positive", "constructive")
        assert result.sentiment_score >= 4

    def test_positive_english(self, classifier):
        result = classifier.analyze("Great content! I really enjoyed watching this.")
        assert result.category in ("positive", "constructive")
        assert result.sentiment_score >= 4

    def test_constructive_chinese(self, classifier):
        result = classifier.analyze("内容不错，建议增加一些实际案例来辅助说明，这样会更容易理解。")
        assert result.is_constructive is True
        assert result.category == "constructive"

    def test_constructive_english(self, classifier):
        result = classifier.analyze(
            "Great video! I suggest adding timestamps, it would improve navigation."
        )
        assert result.is_constructive is True
        assert result.category == "constructive"


class TestEdgeCases:
    """测试边界情况。"""

    def test_empty_string(self, classifier):
        result = classifier.analyze("")
        assert result.category == "neutral"
        assert result.confidence == 1.0

    def test_whitespace_only(self, classifier):
        result = classifier.analyze("   ")
        assert result.category == "neutral"

    def test_single_character(self, classifier):
        result = classifier.analyze("a")
        assert result.category is not None

    def test_long_text(self, classifier):
        long_text = "这是一段很长的评论。" * 100
        result = classifier.analyze(long_text)
        assert result.category is not None
        assert 1 <= result.sentiment_score <= 5


class TestBatchAnalysis:
    """测试批量分析。"""

    def test_batch(self, classifier):
        texts = ["太棒了！", "垃圾内容", "还行吧"]
        results = classifier.analyze_batch(texts)
        assert len(results) == 3
        for r in results:
            assert r.category in ("toxic", "negative", "neutral", "positive", "constructive")

    def test_empty_batch(self, classifier):
        results = classifier.analyze_batch([])
        assert len(results) == 0
