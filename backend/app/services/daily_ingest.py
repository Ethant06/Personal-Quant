"""
Daily news scrape + digest build for every user with a watchlist.
"""
from __future__ import annotations

from datetime import date, datetime, timezone

from sqlalchemy import text

from app.database import engine
from app.services.article_store import upsert_headlines
from app.services.briefing_builder import build_items_for_tickers
from app.services.briefing_store import (
    persist_briefing,
    users_with_watchlists,
    watchlist_tickers,
)
from app.services.news import NewsHeadline, scrape_tickers


def all_watched_tickers() -> list[str]:
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT DISTINCT c.ticker
                FROM investory.watchlist_items AS w
                JOIN investory.companies AS c ON c.id = w.company_id
                ORDER BY c.ticker
                """
            )
        ).mappings().all()
    return [row["ticker"] for row in rows]


def scrape_watchlist_news(per_ticker: int = 5) -> dict:
    """
    Step 1: scrape public feeds for every ticker anyone follows, upsert articles.
    """
    tickers = all_watched_tickers()
    by_ticker = scrape_tickers(tickers, per_ticker=per_ticker)
    flat: list[NewsHeadline] = []
    for headlines in by_ticker.values():
        flat.extend(headlines)
    store_stats = upsert_headlines(flat)
    return {
        "tickers": tickers,
        "ticker_counts": {t: len(hs) for t, hs in by_ticker.items()},
        **store_stats,
    }


def ingest_user(user_id: str, per_ticker: int = 2) -> dict:
    today = date.today().isoformat()
    tickers = watchlist_tickers(user_id)
    if not tickers:
        return {
            "user_id": user_id,
            "date": today,
            "status": "empty",
            "tickers": 0,
            "items": 0,
        }

    items = build_items_for_tickers(tickers, per_ticker=per_ticker)
    note = (
        f"Daily news scrape at {datetime.now(timezone.utc).isoformat()} "
        f"from Yahoo RSS/search (+ Google News fallback) for: {', '.join(tickers)}. "
        "Educational only — not investment advice."
    )
    persist_briefing(user_id, today, items, note)
    return {
        "user_id": user_id,
        "date": today,
        "status": "ready",
        "tickers": len(tickers),
        "items": len(items),
    }


def run_daily_ingest(per_ticker: int = 5) -> dict:
    """
    Full daily pipeline:
      1) scrape + store articles for all watched tickers
      2) rebuild each user's daily briefing from fresh headlines
    """
    scrape = scrape_watchlist_news(per_ticker=per_ticker)
    user_ids = users_with_watchlists()
    # Briefing cards stay short; scrape stores more articles than we surface
    results = [ingest_user(user_id, per_ticker=min(2, per_ticker)) for user_id in user_ids]
    return {
        "date": date.today().isoformat(),
        "scrape": scrape,
        "users": len(user_ids),
        "results": results,
    }
