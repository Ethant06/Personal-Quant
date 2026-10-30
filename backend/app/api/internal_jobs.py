"""
Secured job triggers for cron / Railway.

Send header: X-Job-Secret: <INTERNAL_JOB_SECRET>
"""
from fastapi import APIRouter, Header, HTTPException

from app.core.config import INTERNAL_JOB_SECRET
from app.services.daily_ingest import run_daily_ingest, scrape_watchlist_news

router = APIRouter(prefix="/internal/jobs", tags=["internal"])


def _require_secret(x_job_secret: str | None) -> None:
    if not INTERNAL_JOB_SECRET:
        raise HTTPException(
            status_code=503,
            detail="INTERNAL_JOB_SECRET is not configured on the server",
        )
    if not x_job_secret or x_job_secret != INTERNAL_JOB_SECRET:
        raise HTTPException(status_code=401, detail="Invalid job secret")


@router.post("/news-scrape")
def news_scrape(x_job_secret: str | None = Header(default=None)):
    """Scrape + store articles for all watched tickers (no briefing rebuild)."""
    _require_secret(x_job_secret)
    return scrape_watchlist_news()


@router.post("/daily-ingest")
def daily_ingest(x_job_secret: str | None = Header(default=None)):
    """Scrape news for watched tickers, then rebuild each user's daily digest."""
    _require_secret(x_job_secret)
    return run_daily_ingest()
