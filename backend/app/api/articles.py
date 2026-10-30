from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import text

from app.auth.deps import get_current_profile
from app.database import engine
from app.schemas.articles import ArticleOut
from app.services.classify import CATEGORIES

router = APIRouter(prefix="/articles", tags=["articles"])


def _row_to_article(row) -> ArticleOut:
    return ArticleOut(
        id=str(row["id"]),
        ticker=row["ticker"],
        title=row["title"],
        url=row["url"],
        summary=row["summary"],
        provider=row["provider"],
        category=row["category"] or "other",
        published_at=row["published_at"].isoformat() if row.get("published_at") else None,
        created_at=row["created_at"].isoformat() if row.get("created_at") else None,
        confidence=float(row["confidence"]) if row.get("confidence") is not None else None,
    )


@router.get("", response_model=list[ArticleOut])
def list_articles(
    ticker: str | None = Query(default=None, max_length=16),
    category: str | None = Query(default=None, max_length=64),
    limit: int = Query(default=25, ge=1, le=100),
    _profile: dict = Depends(get_current_profile),
):
    if category and category not in CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown category. Allowed: {', '.join(CATEGORIES)}",
        )

    clauses = ["1=1"]
    params: dict = {"limit": limit}
    if ticker:
        clauses.append("a.ticker = :ticker")
        params["ticker"] = ticker.strip().upper()
    if category:
        clauses.append("a.category = :category")
        params["category"] = category

    where = " AND ".join(clauses)
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                f"""
                SELECT
                    a.id, a.ticker, a.title, a.url, a.summary, a.provider,
                    a.category, a.published_at, a.created_at,
                    c.confidence
                FROM investory.articles AS a
                LEFT JOIN investory.classifications AS c ON c.article_id = a.id
                WHERE {where}
                ORDER BY COALESCE(a.published_at, a.created_at) DESC
                LIMIT :limit
                """
            ),
            params,
        ).mappings().all()
    return [_row_to_article(row) for row in rows]


@router.get("/{article_id}", response_model=ArticleOut)
def get_article(
    article_id: str,
    _profile: dict = Depends(get_current_profile),
):
    with engine.connect() as conn:
        row = conn.execute(
            text(
                """
                SELECT
                    a.id, a.ticker, a.title, a.url, a.summary, a.provider,
                    a.category, a.published_at, a.created_at,
                    c.confidence
                FROM investory.articles AS a
                LEFT JOIN investory.classifications AS c ON c.article_id = a.id
                WHERE a.id = :id
                """
            ),
            {"id": article_id},
        ).mappings().first()
    if row is None:
        raise HTTPException(status_code=404, detail="Article not found")
    return _row_to_article(row)
