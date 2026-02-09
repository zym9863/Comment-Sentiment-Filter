import json
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .classifier import CommentClassifier
from .schemas import BatchRequest, BatchResult, CommentRequest, CommentResult

classifier: CommentClassifier | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global classifier
    print("正在加载 BERT 模型，首次运行需要下载约 700MB...")
    classifier = CommentClassifier()
    print("BERT 模型加载完成!")
    yield
    classifier = None


app = FastAPI(
    title="评论区情感过滤器",
    description="基于 BERT 的评论情感分析与恶意内容过滤 API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/analyze", response_model=CommentResult)
async def analyze_comment(req: CommentRequest):
    return classifier.analyze(req.text)


@app.post("/api/analyze/batch", response_model=BatchResult)
async def analyze_batch(req: BatchRequest):
    texts = [c.text for c in req.comments]
    results = classifier.analyze_batch(texts)
    return BatchResult(results=results)


@app.get("/api/samples")
async def get_samples():
    samples_path = Path(__file__).parent.parent / "data" / "sample_comments.json"
    with open(samples_path, encoding="utf-8") as f:
        return json.load(f)


@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "model_loaded": classifier is not None,
    }
