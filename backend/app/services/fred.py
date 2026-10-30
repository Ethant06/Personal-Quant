"""
FRED macro series (educational context). Requires FRED_API_KEY for live data.
"""
from __future__ import annotations

from dataclasses import dataclass

import requests

from app.core.config import FRED_API_KEY

# Curated beginner-relevant series
DEFAULT_SERIES: tuple[tuple[str, str, str], ...] = (
    ("FEDFUNDS", "Federal Funds Rate", "interest_rates"),
    ("CPIAUCSL", "Consumer Price Index", "inflation"),
    ("UNRATE", "Unemployment Rate", "other"),
    ("DCOILWTICO", "WTI Crude Oil Price", "other"),
)


@dataclass(frozen=True)
class MacroIndicator:
    series_id: str
    title: str
    theme: str
    latest_value: str | None
    latest_date: str | None
    source_url: str
    note: str


def _fetch_observations(series_id: str) -> tuple[str | None, str | None]:
    if not FRED_API_KEY:
        return None, None
    try:
        response = requests.get(
            "https://api.stlouisfed.org/fred/series/observations",
            params={
                "series_id": series_id,
                "api_key": FRED_API_KEY,
                "file_type": "json",
                "sort_order": "desc",
                "limit": 5,
            },
            timeout=15,
        )
        response.raise_for_status()
        observations = response.json().get("observations") or []
    except (requests.RequestException, ValueError):
        return None, None

    for obs in observations:
        value = obs.get("value")
        if value is None or value == ".":
            continue
        return str(value), obs.get("date")
    return None, None


def list_macro_indicators() -> list[MacroIndicator]:
    indicators: list[MacroIndicator] = []
    for series_id, title, theme in DEFAULT_SERIES:
        value, as_of = _fetch_observations(series_id)
        source = f"https://fred.stlouisfed.org/series/{series_id}"
        if value is None:
            note = (
                "Live FRED value unavailable (set FRED_API_KEY for numbers). "
                "Open the source to explore the series yourself — educational only."
            )
        else:
            note = (
                "Latest published observation from FRED. Context for learning, "
                "not a forecast or trading signal."
            )
        indicators.append(
            MacroIndicator(
                series_id=series_id,
                title=title,
                theme=theme,
                latest_value=value,
                latest_date=as_of,
                source_url=source,
                note=note,
            )
        )
    return indicators
