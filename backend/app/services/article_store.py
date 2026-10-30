"""
Persist scraped headlines into investory.articles (+ classifications).
"""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import text

from app.database import engine
from app.services.classify import classify_headline, normalize_text
from app.services.news import NewsHeadline


def _parse_published(value: str | None):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def upsert_headlines(headlines: list[NewsHeadline]) -> dict:
    upserted = 0
    with engine.begin() as conn:
        for h in headlines:
            category, confidence = classify_headline(h.title, h.summary)
            published = _parse_published(h.published_at)
            row = conn.execute(
                text(
                    """
                    INSERT INTO investory.articles (
                        ticker, title, title_norm, url, summary, provider,
                        category, published_at
                    )
                    VALUES (
                        :ticker, :title, :title_norm, :url, :summary, :provider,
                        :category, :published_at
                    )
                    ON CONFLICT (url) DO UPDATE
                        SET title = EXCLUDED.title,
                            title_norm = EXCLUDED.title_norm,
                            summary = COALESCE(EXCLUDED.summary, investory.articles.summary),
                            ticker = COALESCE(EXCLUDED.ticker, investory.articles.ticker),
                            category = EXCLUDED.category,
                            provider = EXCLUDED.provider,
                            published_at = COALESCE(EXCLUDED.published_at, investory.articles.published_at)
                    RETURNING id
                    """
                ),
                {
                    "ticker": h.ticker,
                    "title": h.title,
                    "title_norm": normalize_text(h.title),
                    "url": h.url,
                    "summary": h.summary,
                    "provider": h.provider,
                    "category": category,
                    "published_at": published,
                },
            ).mappings().first()
            if row is None:
                continue
            upserted += 1
            conn.execute(
                text(
                    """
                    INSERT INTO investory.classifications (
                        article_id, category, confidence, model
                    )
                    VALUES (:article_id, :category, :confidence, 'heuristic_v1')
                    ON CONFLICT (article_id) DO UPDATE
                        SET category = EXCLUDED.category,
                            confidence = EXCLUDED.confidence,
                            created_at = now()
                    """
                ),
                {
                    "article_id": row["id"],
                    "category": category,
                    "confidence": confidence,
                },
            )
    return {
        "scraped_at": datetime.now(timezone.utc).isoformat(),
        "headlines": len(headlines),
        "upserted": upserted,
    }
