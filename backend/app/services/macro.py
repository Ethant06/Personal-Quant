"""
Macro / politics educational signals that may relate to a company.

Uses public Yahoo search for a few themes (oil, rates, geopolitics).
Not investment advice — context for beginners only.
"""
from __future__ import annotations

from dataclasses import dataclass

import requests


@dataclass(frozen=True)
class MacroSignal:
    theme: str
    headline: str
    why_it_may_matter: str
    source_url: str | None


_THEMES: list[tuple[str, str, str]] = [
    (
        "oil_energy",
        "crude oil prices",
        "Energy and commodity moves can change costs or demand for many businesses, "
        "even companies that are not oil producers.",
    ),
    (
        "interest_rates",
        "Federal Reserve interest rates",
        "Interest-rate expectations affect borrowing costs, consumer spending, "
        "and how investors value future company cash flows.",
    ),
    (
        "geopolitics",
        "geopolitical risk markets",
        "Conflicts and policy shocks can disrupt supply chains, trade, "
        "and risk appetite — relevant context when reading company news.",
    ),
]


def _yahoo_search_headline(query: str) -> tuple[str, str] | None:
    try:
        response = requests.get(
            "https://query1.finance.yahoo.com/v1/finance/search",
            params={
                "q": query,
                "quotesCount": 0,
                "newsCount": 1,
                "listsCount": 0,
            },
            headers={"User-Agent": "InvestoryDemo/1.0"},
            timeout=12,
        )
        response.raise_for_status()
        news = (response.json().get("news") or [])
    except (requests.RequestException, ValueError):
        return None
    if not news:
        return None
    item = news[0]
    title = item.get("title")
    link = item.get("link")
    if not title:
        return None
    return title, link


def build_macro_signals(ticker: str, limit: int = 3) -> list[MacroSignal]:
    ticker = ticker.strip().upper()
    signals: list[MacroSignal] = []
    for theme, query, why in _THEMES:
        found = _yahoo_search_headline(query)
        if found:
            headline, url = found
            signals.append(
                MacroSignal(
                    theme=theme,
                    headline=headline,
                    why_it_may_matter=(
                        f"For someone following {ticker}: {why} "
                        "Read the source and decide what (if anything) connects."
                    ),
                    source_url=url,
                )
            )
        else:
            signals.append(
                MacroSignal(
                    theme=theme,
                    headline=f"{theme.replace('_', ' ').title()} — no live headline right now",
                    why_it_may_matter=(
                        f"For someone following {ticker}: {why} "
                        "Try again after the daily refresh."
                    ),
                    source_url=None,
                )
            )
        if len(signals) >= limit:
            break
    return signals
