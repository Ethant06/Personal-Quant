from pydantic import BaseModel, Field

from app.schemas.companies import CompanyOut


class WatchlistItemOut(BaseModel):
    id: str
    created_at: str | None = None
    company: CompanyOut
    today_item_count: int = 0
    last_briefing_at: str | None = None


class WatchlistAdd(BaseModel):
    """Add by company id, or by ticker (upserts company if name provided)."""

    company_id: str | None = None
    ticker: str | None = Field(default=None, max_length=16)
    name: str | None = Field(default=None, max_length=200)
    exchange: str | None = Field(default=None, max_length=32)
