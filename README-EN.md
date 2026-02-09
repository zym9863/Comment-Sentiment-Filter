English | [中文](README.md)

# Comment Sentiment Filter

A BERT-based sentiment analysis and content filtering service for Chinese and English comments. It detects toxic comments, highlights constructive feedback, and provides a clean web UI for exploration.

**Features**
- Sentiment analysis for CN/EN comments with categories `toxic | negative | neutral | positive | constructive`
- Toxic detection: low sentiment score + keyword hits
- Constructive detection: high sentiment score + keyword hits
- Single and batch analysis APIs
- Frontend filtering, stats, and sample loading

**Tech Stack**
- Backend: FastAPI + Transformers + PyTorch
- Frontend: Svelte 5 + Vite
- Model: `nlptown/bert-base-multilingual-uncased-sentiment`

**Quick Start**
1. Install backend dependencies (choose one)
   - Using `uv` (recommended)
     ```bash
     uv sync
     ```
   - Using `pip`
     ```bash
     pip install -e .
     ```
2. Start backend
   ```bash
   uv run python main.py
   ```
   The first run downloads about 700MB of model weights.
3. Start frontend
   ```bash
   cd frontend
   pnpm install
   pnpm dev
   ```
   The frontend proxies `/api` to `http://localhost:8000`.

**API**
- `POST /api/analyze`
  - Body: `{"text": "your comment"}`
  - Returns: `CommentResult`
- `POST /api/analyze/batch`
  - Body: `{"comments": [{"text": "..."}, {"text": "..."}]}`
  - Returns: `{"results": [CommentResult, ...]}`
- `GET /api/samples`
  - Returns built-in sample comments
- `GET /api/health`
  - Returns service status and model load state

`CommentResult` schema
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

**Training & Evaluation**
- Train
  ```bash
  uv run python -m training.train --data data/train.json --epochs 5
  ```
- Evaluate
  ```bash
  uv run python -m training.evaluate --model model_cache/finetuned --data data/test.json
  ```
- Data format (JSON)
  ```json
  [
    { "text": "comment", "label": "toxic|negative|neutral|positive|constructive" }
  ]
  ```

**Tests**
```bash
uv run pytest
```
Tests will trigger model download and loading.

**Project Structure**
- `app/`: FastAPI service and classification logic
- `training/`: fine-tuning and evaluation scripts
- `data/`: sample data
- `frontend/`: Svelte frontend
