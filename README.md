[English](README-EN.md) | 中文

# Comment Sentiment Filter（评论区情感过滤器）

基于 BERT 的中英文评论情感分析与内容过滤服务，支持识别恶意评论、建设性反馈与常规情感分类，并提供简洁的前端可视化界面。

**功能概览**
- 中英文评论情感分析，输出 `toxic | negative | neutral | positive | constructive`
- 恶意评论检测：低情感分 + 关键词命中
- 建设性反馈识别：高情感分 + 关键词命中
- 单条与批量分析 API
- 前端支持筛选、统计与样本加载

**技术栈**
- 后端：FastAPI + Transformers + PyTorch
- 前端：Svelte 5 + Vite
- 模型：`nlptown/bert-base-multilingual-uncased-sentiment`

**快速开始**
1. 后端安装依赖（二选一）
   - 使用 `uv`（推荐）
     ```bash
     uv sync
     ```
   - 使用 `pip`
     ```bash
     pip install -e .
     ```
2. 启动后端
   ```bash
   uv run python main.py
   ```
   首次运行会下载约 700MB 的 BERT 模型，请确保网络通畅。
3. 启动前端
   ```bash
   cd frontend
   pnpm install
   pnpm dev
   ```
   前端默认通过 Vite 代理访问 `http://localhost:8000/api`。

**API 说明**
- `POST /api/analyze`
  - 请求体：`{"text": "你的评论"}`
  - 返回：`CommentResult`
- `POST /api/analyze/batch`
  - 请求体：`{"comments": [{"text": "..."}, {"text": "..."}]}`
  - 返回：`{"results": [CommentResult, ...]}`
- `GET /api/samples`
  - 返回内置样本评论列表
- `GET /api/health`
  - 返回服务状态与模型加载情况

`CommentResult` 结构
```json
{
  "text": "string",
  "category": "toxic|negative|neutral|positive|constructive",
  "confidence": 0.0,
  "sentiment_score": 1,
  "is_toxic": false,
  "is_constructive": false
}
```

**训练与评估**
- 训练
  ```bash
  uv run python -m training.train --data data/train.json --epochs 5
  ```
- 评估
  ```bash
  uv run python -m training.evaluate --model model_cache/finetuned --data data/test.json
  ```
- 数据格式（JSON）
  ```json
  [
    { "text": "评论内容", "label": "toxic|negative|neutral|positive|constructive" }
  ]
  ```

**测试**
```bash
uv run pytest
```
测试会触发模型下载与加载，请预留时间与网络带宽。

**项目结构**
- `app/`：FastAPI 服务与分类逻辑
- `training/`：微调与评估脚本
- `data/`：样本数据
- `frontend/`：Svelte 前端
