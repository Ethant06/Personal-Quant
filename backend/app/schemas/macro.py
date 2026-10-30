from pydantic import BaseModel


class MacroIndicatorOut(BaseModel):
    series_id: str
    title: str
    theme: str
    latest_value: str | None = None
    latest_date: str | None = None
    source_url: str
    note: str
