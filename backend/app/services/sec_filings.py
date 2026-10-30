"""
Best-effort recent SEC EDGAR filings for a ticker (public data.sec.gov).

Educational links only — no scores or investment signals.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

import requests

_SEC_HEADERS = {
    "User-Agent": "InvestoryDemo contact@investory.local",
    "Accept-Encoding": "gzip, deflate",
}


@dataclass(frozen=True)
class SecFiling:
    form: str
    title: str
    url: str
    filed_at: str | None


@lru_cache(maxsize=1)
def _ticker_to_cik() -> dict[str, str]:
    try:
        response = requests.get(
            "https://www.sec.gov/files/company_tickers.json",
            headers=_SEC_HEADERS,
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError):
        return {}

    mapping: dict[str, str] = {}
    for entry in payload.values():
        ticker = str(entry.get("ticker") or "").upper()
        cik = entry.get("cik_str")
        if ticker and cik is not None:
            mapping[ticker] = str(cik).zfill(10)
    return mapping


def fetch_recent_filings(ticker: str, limit: int = 5) -> list[SecFiling]:
    ticker = ticker.strip().upper()
    cik = _ticker_to_cik().get(ticker)
    if not cik:
        return []

    try:
        response = requests.get(
            f"https://data.sec.gov/submissions/CIK{cik}.json",
            headers=_SEC_HEADERS,
            timeout=20,
        )
        response.raise_for_status()
        payload = response.json()
    except (requests.RequestException, ValueError):
        return []

    recent = (payload.get("filings") or {}).get("recent") or {}
    forms = recent.get("form") or []
    accessions = recent.get("accessionNumber") or []
    primaries = recent.get("primaryDocument") or []
    dates = recent.get("filingDate") or []
    descriptions = recent.get("primaryDocDescription") or []

    wanted = {"8-K", "10-Q", "10-K", "6-K", "20-F"}
    filings: list[SecFiling] = []
    for i, form in enumerate(forms):
        if form not in wanted:
            continue
        if i >= len(accessions) or i >= len(primaries):
            continue
        accession = accessions[i].replace("-", "")
        doc = primaries[i]
        url = f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{accession}/{doc}"
        title = descriptions[i] if i < len(descriptions) and descriptions[i] else f"{form} filing"
        filed_at = dates[i] if i < len(dates) else None
        filings.append(SecFiling(form=form, title=title, url=url, filed_at=filed_at))
        if len(filings) >= limit:
            break
    return filings
