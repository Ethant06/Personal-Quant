from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query

from app.auth.deps import get_current_profile
from app.schemas.briefings import BriefingOut
from app.services.briefing_builder import build_items_for_tickers
from app.services.briefing_store import (
    load_briefing,
    persist_briefing,
    watchlist_tickers,
)
from app.services.classify import CATEGORIES

router = APIRouter(prefix="/briefings", tags=["briefings"])


@router.get("/today", response_model=BriefingOut)
def get_today_briefing(
    category: str | None = Query(default=None, max_length=64),
    profile: dict = Depends(get_current_profile),
):
    if category and category not in CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown category. Allowed: {', '.join(CATEGORIES)}",
        )

    today = date.today().isoformat()
    saved = load_briefing(profile["id"], today)
    if saved and saved.items:
        items = saved.items
        if category:
            items = [i for i in items if i.category == category]
        return BriefingOut(
            date=saved.date,
            status=saved.status,
            items=items,
            note=saved.note,
        )

    tickers = watchlist_tickers(profile["id"])
    if not tickers:
        return BriefingOut(
            date=today,
            status="empty",
            items=[],
            note="Add companies to your watchlist. Daily refresh fills updates automatically.",
        )

    return BriefingOut(
        date=today,
        status="pending",
        items=[],
        note="No daily digest yet. Updates appear after the nightly refresh.",
    )


@router.post("/generate", response_model=BriefingOut)
def generate_briefing(profile: dict = Depends(get_current_profile)):
    """Manual regenerate for demos/admin. Happy path is the daily ingest job."""
    today = date.today().isoformat()
    tickers = watchlist_tickers(profile["id"])
    if not tickers:
        return BriefingOut(
            date=today,
            status="empty",
            items=[],
            note="Add companies to your watchlist before generating a briefing.",
        )

    items = build_items_for_tickers(tickers, per_ticker=2)
    note = (
        f"Generated at {datetime.now(timezone.utc).isoformat()} from public headlines "
        f"(Yahoo search) for: {', '.join(tickers)}. Educational only — not investment advice."
    )
    persist_briefing(profile["id"], today, items, note)
    return BriefingOut(date=today, status="ready", items=items, note=note)
