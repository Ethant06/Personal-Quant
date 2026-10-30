from pydantic import BaseModel


class BriefingItemOut(BaseModel):
    id: str
    ticker: str | None = None
    category: str
    headline: str
    what_happened: str
    why_it_matters: str
    macro_link: str | None = None
    terms: list[str] = []
    uncertainties: str
    facts: list[str] = []
    implications: list[str] = []
    source_urls: list[str] = []


class BriefingOut(BaseModel):
    date: str
    status: str
    items: list[BriefingItemOut]
    note: str | None = None
