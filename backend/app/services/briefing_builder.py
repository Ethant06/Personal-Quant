"""
Build beginner-friendly briefing items from headlines (and optional LLM later).

No buy/sell language. Educational framing only.
"""
from __future__ import annotations

from uuid import uuid4

from app.schemas.briefings import BriefingItemOut
from app.services.classify import (
    beginner_terms_for,
    classify_headline,
    macro_blurb_for,
)
from app.services.dedupe import is_near_duplicate
from app.services.news import fetch_latest_headlines
from app.services.safety import strip_advice_language


def _item_from_headline(h) -> BriefingItemOut:
    category, _confidence = classify_headline(h.title, h.summary)
    summary = (h.summary or "").strip()
    what = strip_advice_language(summary or h.title)
    return BriefingItemOut(
        id=str(uuid4()),
        ticker=h.ticker,
        category=category,
        headline=h.title,
        what_happened=what,
        why_it_matters=strip_advice_language(
            f"This story may matter to people following {h.ticker} because "
            "company news can change how investors understand the business. "
            "Read the source and decide what (if anything) it means for your learning."
        ),
        macro_link=macro_blurb_for(category),
        terms=beginner_terms_for(category),
        uncertainties=(
            "Headlines can be incomplete or outdated. This summary is educational, "
            "not verified financial analysis, and not investment advice."
        ),
        facts=[h.title],
        implications=[
            "Possible implication only: the market or the company's narrative may "
            "react — or it may not. Treat this as a learning prompt.",
        ],
        source_urls=[h.url],
    )


def _fallback_item(ticker: str) -> BriefingItemOut:
    return BriefingItemOut(
        id=str(uuid4()),
        ticker=ticker,
        category="other",
        headline=f"{ticker}: no live headline available right now",
        what_happened=(
            f"We could not pull a fresh public headline for {ticker}. "
            "Your watchlist still works — updates appear after the next daily refresh."
        ),
        why_it_matters=(
            "A working watchlist + briefing layout is still useful for learning "
            "how Investory will present real developments."
        ),
        macro_link=macro_blurb_for("other"),
        terms=beginner_terms_for("other"),
        uncertainties="No primary source was retrieved for this ticker in this run.",
        facts=[f"{ticker} is on your watchlist."],
        implications=["No investment advice — educational placeholder."],
        source_urls=[],
    )


def build_items_for_tickers(tickers: list[str], per_ticker: int = 2) -> list[BriefingItemOut]:
    items: list[BriefingItemOut] = []
    for ticker in tickers[:6]:
        headlines = fetch_latest_headlines(ticker, limit=per_ticker)
        if headlines:
            items.extend(_item_from_headline(h) for h in headlines)
        else:
            items.append(_fallback_item(ticker))

    final: list[BriefingItemOut] = []
    for item in items:
        if any(
            item.headline
            and existing.headline
            and is_near_duplicate(item.headline, existing.headline)
            for existing in final
        ):
            continue
        final.append(item)
    return final
