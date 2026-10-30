from pydantic import BaseModel


class ArticleOut(BaseModel):
    id: str
    ticker: str | None = None
    title: str
    url: str
    summary: str | None = None
    provider: str
    category: str = "other"
    published_at: str | None = None
    created_at: str | None = None
    confidence: float | None = None
