"""API 集成测试。"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


class TestHealthEndpoint:
    def test_health(self, client):
        res = client.get("/api/health")
        assert res.status_code == 200
        data = res.json()
        assert data["status"] == "ok"
        assert data["model_loaded"] is True


class TestAnalyzeEndpoint:
    def test_analyze_single(self, client):
        res = client.post("/api/analyze", json={"text": "这是一条测试评论"})
        assert res.status_code == 200
        data = res.json()
        assert "category" in data
        assert "confidence" in data
        assert "sentiment_score" in data
        assert data["category"] in ("toxic", "negative", "neutral", "positive", "constructive")
        assert 0 <= data["confidence"] <= 1
        assert 1 <= data["sentiment_score"] <= 5

    def test_analyze_empty(self, client):
        res = client.post("/api/analyze", json={"text": ""})
        assert res.status_code == 200
        assert res.json()["category"] == "neutral"

    def test_analyze_missing_text(self, client):
        res = client.post("/api/analyze", json={})
        assert res.status_code == 422


class TestBatchEndpoint:
    def test_batch_analyze(self, client):
        res = client.post(
            "/api/analyze/batch",
            json={"comments": [{"text": "好评"}, {"text": "差评"}]},
        )
        assert res.status_code == 200
        data = res.json()
        assert len(data["results"]) == 2

    def test_batch_empty(self, client):
        res = client.post("/api/analyze/batch", json={"comments": []})
        assert res.status_code == 200
        assert len(res.json()["results"]) == 0


class TestSamplesEndpoint:
    def test_get_samples(self, client):
        res = client.get("/api/samples")
        assert res.status_code == 200
        data = res.json()
        assert isinstance(data, list)
        assert len(data) > 0
        assert "text" in data[0]
