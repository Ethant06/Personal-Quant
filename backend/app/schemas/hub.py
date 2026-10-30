from pydantic import BaseModel

from app.schemas.briefings import BriefingItemOut
from app.schemas.companies import CompanyOut


class ArticleOut(BaseModel):
    id: str
    title: str
    url: str
    summary: str | None = None
    provider: str
    category: str = "other"
    published_at: str | None = None


class FilingOut(BaseModel):
    form: str
    title: str
    url: str
    filed_at: str | None = None


class MacroSignalOut(BaseModel):
    theme: str
    headline: str
    why_it_may_matter: str
    source_url: str | None = None


class CompanyHubOut(BaseModel):
    company: CompanyOut
    briefing_date: str | None = None
    status: str
    note: str | None = None
    items: list[BriefingItemOut] = []
    articles: list[ArticleOut] = []
    filings: list[FilingOut] = []
    macro_signals: list[MacroSignalOut] = []
