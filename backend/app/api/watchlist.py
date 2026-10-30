from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text

from app.auth.deps import get_current_profile
from app.database import engine
from app.schemas.companies import CompanyOut
from app.schemas.watchlist import WatchlistAdd, WatchlistItemOut
from app.services.briefing_store import (
    latest_briefing_timestamp,
    ticker_item_counts_for_today,
)

router = APIRouter(prefix="/watchlist", tags=["watchlist"])


def _item_from_row(
    row,
    *,
    today_item_count: int = 0,
    last_briefing_at: str | None = None,
) -> WatchlistItemOut:
    return WatchlistItemOut(
        id=str(row["id"]),
        created_at=row["created_at"].isoformat() if row["created_at"] else None,
        company=CompanyOut(
            id=str(row["company_id"]),
            ticker=row["ticker"],
            name=row["name"],
            exchange=row["exchange"],
        ),
        today_item_count=today_item_count,
        last_briefing_at=last_briefing_at,
    )


@router.get("", response_model=list[WatchlistItemOut])
def list_watchlist(profile: dict = Depends(get_current_profile)):
    counts = ticker_item_counts_for_today(profile["id"])
    last_at = latest_briefing_timestamp(profile["id"])
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT
                    w.id,
                    w.created_at,
                    c.id AS company_id,
                    c.ticker,
                    c.name,
                    c.exchange
                FROM investory.watchlist_items AS w
                JOIN investory.companies AS c ON c.id = w.company_id
                WHERE w.user_id = :user_id
                ORDER BY w.created_at DESC
                """
            ),
            {"user_id": profile["id"]},
        ).mappings().all()
    return [
        _item_from_row(
            row,
            today_item_count=counts.get((row["ticker"] or "").upper(), 0),
            last_briefing_at=last_at,
        )
        for row in rows
    ]


@router.post("", response_model=WatchlistItemOut, status_code=201)
def add_to_watchlist(
    body: WatchlistAdd,
    profile: dict = Depends(get_current_profile),
):
    company_id = body.company_id
    last_at = latest_briefing_timestamp(profile["id"])

    with engine.begin() as conn:
        if company_id is None:
            if not body.ticker:
                raise HTTPException(
                    status_code=400,
                    detail="Provide company_id or ticker",
                )
            ticker = body.ticker.strip().upper()
            name = (body.name or ticker).strip()
            row = conn.execute(
                text(
                    """
                    INSERT INTO investory.companies (ticker, name, exchange)
                    VALUES (:ticker, :name, :exchange)
                    ON CONFLICT (ticker) DO UPDATE
                        SET name = COALESCE(EXCLUDED.name, investory.companies.name),
                            exchange = COALESCE(EXCLUDED.exchange, investory.companies.exchange),
                            updated_at = now()
                    RETURNING id
                    """
                ),
                {
                    "ticker": ticker,
                    "name": name,
                    "exchange": body.exchange.strip() if body.exchange else None,
                },
            ).mappings().first()
            company_id = str(row["id"])

        company = conn.execute(
            text(
                """
                SELECT id, ticker, name, exchange
                FROM investory.companies
                WHERE id = :id
                """
            ),
            {"id": company_id},
        ).mappings().first()
        if company is None:
            raise HTTPException(status_code=404, detail="Company not found")

        existing = conn.execute(
            text(
                """
                SELECT w.id, w.created_at, c.id AS company_id, c.ticker, c.name, c.exchange
                FROM investory.watchlist_items AS w
                JOIN investory.companies AS c ON c.id = w.company_id
                WHERE w.user_id = :user_id AND w.company_id = :company_id
                """
            ),
            {"user_id": profile["id"], "company_id": company_id},
        ).mappings().first()
        if existing:
            counts = ticker_item_counts_for_today(profile["id"])
            return _item_from_row(
                existing,
                today_item_count=counts.get((existing["ticker"] or "").upper(), 0),
                last_briefing_at=last_at,
            )

        created = conn.execute(
            text(
                """
                INSERT INTO investory.watchlist_items (user_id, company_id)
                VALUES (:user_id, :company_id)
                RETURNING id, created_at
                """
            ),
            {"user_id": profile["id"], "company_id": company_id},
        ).mappings().first()

    return WatchlistItemOut(
        id=str(created["id"]),
        created_at=created["created_at"].isoformat() if created["created_at"] else None,
        company=CompanyOut(
            id=str(company["id"]),
            ticker=company["ticker"],
            name=company["name"],
            exchange=company["exchange"],
        ),
        today_item_count=0,
        last_briefing_at=last_at,
    )


@router.delete("/{item_id}", status_code=204)
def remove_from_watchlist(
    item_id: str,
    profile: dict = Depends(get_current_profile),
):
    with engine.begin() as conn:
        result = conn.execute(
            text(
                """
                DELETE FROM investory.watchlist_items
                WHERE id = :id AND user_id = :user_id
                """
            ),
            {"id": item_id, "user_id": profile["id"]},
        )
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Watchlist item not found")
    return None
