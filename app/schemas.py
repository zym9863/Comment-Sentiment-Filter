from pydantic import BaseModel


class CommentRequest(BaseModel):
    text: str


class BatchRequest(BaseModel):
    comments: list[CommentRequest]


class CommentResult(BaseModel):
    text: str
    category: str  # toxic | negative | neutral | positive | constructive
    confidence: float
    sentiment_score: int  # 1-5 星
    is_toxic: bool
    is_constructive: bool


class BatchResult(BaseModel):
    results: list[CommentResult]
