"""
Persist and load daily briefings / briefing items.

Shared by the briefings API and the daily ingest job.
"""
from __future__ import annotations

from datetime import date

from sqlalchemy import text

from app.database import engine
from app.schemas.briefings import BriefingItemOut, BriefingOut
from app.services.classify import classify_headline, normalize_text


def persist_briefing(
    user_id: str,
    briefing_date: str,
    items: list[BriefingItemOut],
    note: str,
) -> None:
    with engine.begin() as conn:
        briefing = conn.execute(
            text(
                """
                INSERT INTO investory.briefings (user_id, briefing_date, status, note)
                VALUES (:user_id, :briefing_date, 'ready', :note)
                ON CONFLICT (user_id, briefing_date) DO UPDATE
                    SET status = 'ready',
                        note = EXCLUDED.note,
                        created_at = now()
                RETURNING id
                """
            ),
            {
                "user_id": user_id,
                "briefing_date": briefing_date,
                "note": note,
            },
        ).mappings().first()
        if briefing is None:
            return

        conn.execute(
            text("DELETE FROM investory.briefing_items WHERE briefing_id = :id"),
            {"id": briefing["id"]},
        )

        for item in items:
            article_id = None
            if item.source_urls:
                category, confidence = classify_headline(item.headline, item.what_happened)
                # Prefer category already chosen on the briefing item
                category = item.category or category
                article = conn.execute(
                    text(
                        """
                        INSERT INTO investory.articles (
                            ticker, title, title_norm, url, summary, provider, category
                        )
                        VALUES (
                            :ticker, :title, :title_norm, :url, :summary, 'yahoo', :category
                        )
                        ON CONFLICT (url) DO UPDATE
                            SET title = EXCLUDED.title,
                                title_norm = EXCLUDED.title_norm,
                                summary = COALESCE(EXCLUDED.summary, investory.articles.summary),
                                ticker = COALESCE(EXCLUDED.ticker, investory.articles.ticker),
                                category = EXCLUDED.category
                        RETURNING id
                        """
                    ),
                    {
                        "ticker": item.ticker,
                        "title": item.headline,
                        "title_norm": normalize_text(item.headline),
                        "url": item.source_urls[0],
                        "summary": item.what_happened,
                        "category": category,
                    },
                ).mappings().first()
                article_id = article["id"] if article else None
                if article_id is not None:
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
                                    model = EXCLUDED.model,
                                    created_at = now()
                            """
                        ),
                        {
                            "article_id": article_id,
                            "category": category,
                            "confidence": confidence,
                        },
                    )

            conn.execute(
                text(
                    """
                    INSERT INTO investory.briefing_items (
                        briefing_id, article_id, ticker, category, headline,
                        what_happened, why_it_matters, macro_link, terms,
                        uncertainties, facts, implications, source_urls
                    )
                    VALUES (
                        :briefing_id, :article_id, :ticker, :category, :headline,
                        :what_happened, :why_it_matters, :macro_link, :terms,
                        :uncertainties, :facts, :implications, :source_urls
                    )
                    """
                ),
                {
                    "briefing_id": briefing["id"],
                    "article_id": article_id,
                    "ticker": item.ticker,
                    "category": item.category,
                    "headline": item.headline,
                    "what_happened": item.what_happened,
                    "why_it_matters": item.why_it_matters,
                    "macro_link": item.macro_link,
                    "terms": item.terms,
                    "uncertainties": item.uncertainties,
                    "facts": item.facts,
                    "implications": item.implications,
                    "source_urls": item.source_urls,
                },
            )


def load_briefing(user_id: str, briefing_date: str) -> BriefingOut | None:
    with engine.connect() as conn:
        briefing = conn.execute(
            text(
                """
                SELECT id, status, note
                FROM investory.briefings
                WHERE user_id = :user_id AND briefing_date = :briefing_date
                """
            ),
            {"user_id": user_id, "briefing_date": briefing_date},
        ).mappings().first()
        if briefing is None:
            return None

        rows = conn.execute(
            text(
                """
                SELECT
                    id, ticker, category, headline, what_happened, why_it_matters,
                    macro_link, terms, uncertainties, facts, implications, source_urls
                FROM investory.briefing_items
                WHERE briefing_id = :briefing_id
                ORDER BY created_at
                """
            ),
            {"briefing_id": briefing["id"]},
        ).mappings().all()

    items = [
        BriefingItemOut(
            id=str(row["id"]),
            ticker=row["ticker"],
            category=row["category"],
            headline=row["headline"],
            what_happened=row["what_happened"],
            why_it_matters=row["why_it_matters"],
            macro_link=row["macro_link"],
            terms=list(row["terms"] or []),
            uncertainties=row["uncertainties"] or "",
            facts=list(row["facts"] or []),
            implications=list(row["implications"] or []),
            source_urls=list(row["source_urls"] or []),
        )
        for row in rows
    ]
    return BriefingOut(
        date=briefing_date,
        status=briefing["status"],
        items=items,
        note=briefing["note"],
    )


def load_ticker_items(
    user_id: str,
    ticker: str,
    briefing_date: str | None = None,
) -> tuple[BriefingOut | None, list[BriefingItemOut]]:
    """Return today's briefing (if any) and items filtered to one ticker."""
    day = briefing_date or date.today().isoformat()
    briefing = load_briefing(user_id, day)
    if briefing is None:
        return None, []
    ticker_u = ticker.strip().upper()
    items = [i for i in briefing.items if (i.ticker or "").upper() == ticker_u]
    return briefing, items


def watchlist_tickers(user_id: str) -> list[str]:
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT c.ticker
                FROM investory.watchlist_items AS w
                JOIN investory.companies AS c ON c.id = w.company_id
                WHERE w.user_id = :user_id
                ORDER BY w.created_at DESC
                """
            ),
            {"user_id": user_id},
        ).mappings().all()
    return [row["ticker"] for row in rows]


def users_with_watchlists() -> list[str]:
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT DISTINCT user_id::text AS user_id
                FROM investory.watchlist_items
                """
            )
        ).mappings().all()
    return [row["user_id"] for row in rows]


def ticker_item_counts_for_today(user_id: str) -> dict[str, int]:
    today = date.today().isoformat()
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT bi.ticker, COUNT(*)::int AS n
                FROM investory.briefings AS b
                JOIN investory.briefing_items AS bi ON bi.briefing_id = b.id
                WHERE b.user_id = :user_id
                  AND b.briefing_date = :briefing_date
                  AND bi.ticker IS NOT NULL
                GROUP BY bi.ticker
                """
            ),
            {"user_id": user_id, "briefing_date": today},
        ).mappings().all()
    return {(row["ticker"] or "").upper(): row["n"] for row in rows}


def latest_briefing_timestamp(user_id: str) -> str | None:
    with engine.connect() as conn:
        row = conn.execute(
            text(
                """
                SELECT created_at
                FROM investory.briefings
                WHERE user_id = :user_id
                ORDER BY briefing_date DESC, created_at DESC
                LIMIT 1
                """
            ),
            {"user_id": user_id},
        ).mappings().first()
    if row is None or row["created_at"] is None:
        return None
    return row["created_at"].isoformat()
