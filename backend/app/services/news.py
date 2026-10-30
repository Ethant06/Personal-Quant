"""
Daily news pull for watchlist tickers.

This is **public feed / API fetching**, not brittle HTML DOM scraping:
  1. Yahoo Finance RSS (headline?s=TICKER)
  2. Yahoo Finance search JSON
  3. Google News RSS (fallback)

Callers (daily ingest job) should run this on a schedule every day.
"""
from __future__ import annotations

import logging
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus, urlparse, parse_qs, unquote

import requests

from app.services.dedupe import dedupe_headlines

logger = logging.getLogger(__name__)

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; InvestoryBot/1.0; +https://localhost; educational)"
    ),
    "Accept": "application/rss+xml, application/xml, application/json, text/xml, */*",
}


@dataclass(frozen=True)
class NewsHeadline:
    title: str
    url: str
    summary: str | None
    published_at: str | None
    ticker: str
    provider: str = "yahoo"


def _published_iso(raw) -> str | None:
    if raw is None:
        return None
    try:
        if isinstance(raw, (int, float)) or (isinstance(raw, str) and str(raw).isdigit()):
            return datetime.fromtimestamp(int(raw), tz=timezone.utc).isoformat()
    except (OverflowError, OSError, ValueError):
        pass
    if isinstance(raw, str):
        try:
            return parsedate_to_datetime(raw).astimezone(timezone.utc).isoformat()
        except (TypeError, ValueError, IndexError):
            return raw
    return str(raw)


def _get(url: str, *, params: dict | None = None, timeout: int = 15) -> requests.Response | None:
    for attempt in range(3):
        try:
            response = requests.get(
                url,
                params=params,
                headers=_HEADERS,
                timeout=timeout,
            )
            if response.status_code == 429:
                time.sleep(1.5 * (attempt + 1))
                continue
            response.raise_for_status()
            return response
        except requests.RequestException as exc:
            logger.warning("news fetch failed (%s) attempt=%s: %s", url, attempt + 1, exc)
            time.sleep(0.4 * (attempt + 1))
    return None


def _parse_rss_items(xml_text: str) -> list[tuple[str, str, str | None, str | None]]:
    """Return list of (title, link, summary, published)."""
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []

    items: list[tuple[str, str, str | None, str | None]] = []
    # RSS 2.0
    for item in root.findall(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        summary = (item.findtext("description") or None)
        published = item.findtext("pubDate")
        if title and link:
            items.append((title, link, summary, _published_iso(published)))
    # Atom
    if not items:
        ns = {"a": "http://www.w3.org/2005/Atom"}
        for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
            title = (entry.findtext("a:title", default="", namespaces=ns) or "").strip()
            link_el = entry.find("a:link", ns)
            link = (link_el.get("href") if link_el is not None else "") or ""
            summary = entry.findtext("a:summary", default=None, namespaces=ns)
            published = entry.findtext("a:published", default=None, namespaces=ns) or entry.findtext(
                "a:updated", default=None, namespaces=ns
            )
            if title and link:
                items.append((title, link, summary, _published_iso(published)))
    return items


def _unwrap_google_news_url(url: str) -> str:
    """Google News RSS often wraps the real URL in a redirect query."""
    try:
        parsed = urlparse(url)
        if "news.google.com" not in parsed.netloc:
            return url
        qs = parse_qs(parsed.query)
        if "url" in qs and qs["url"]:
            return unquote(qs["url"][0])
    except Exception:
        pass
    return url


def fetch_yahoo_rss(ticker: str, limit: int = 8) -> list[NewsHeadline]:
    ticker = ticker.strip().upper()
    response = _get(
        "https://finance.yahoo.com/rss/headline",
        params={"s": ticker},
    )
    if response is None:
        return []
    headlines: list[NewsHeadline] = []
    for title, link, summary, published in _parse_rss_items(response.text):
        headlines.append(
            NewsHeadline(
                title=title,
                url=link,
                summary=summary,
                published_at=published,
                ticker=ticker,
                provider="yahoo_rss",
            )
        )
        if len(headlines) >= limit:
            break
    return headlines


def fetch_yahoo_search(ticker: str, limit: int = 8) -> list[NewsHeadline]:
    ticker = ticker.strip().upper()
    response = _get(
        "https://query1.finance.yahoo.com/v1/finance/search",
        params={
            "q": ticker,
            "quotesCount": 1,
            "newsCount": limit,
            "listsCount": 0,
        },
    )
    if response is None:
        return []
    try:
        payload = response.json()
    except ValueError:
        return []

    headlines: list[NewsHeadline] = []
    for item in payload.get("news") or []:
        title = item.get("title")
        link = item.get("link")
        if not title or not link:
            continue
        headlines.append(
            NewsHeadline(
                title=title,
                url=link,
                summary=item.get("summary"),
                published_at=_published_iso(item.get("providerPublishTime")),
                ticker=ticker,
                provider="yahoo_search",
            )
        )
        if len(headlines) >= limit:
            break
    return headlines


def fetch_google_news_rss(ticker: str, limit: int = 6) -> list[NewsHeadline]:
    ticker = ticker.strip().upper()
    query = quote_plus(f"{ticker} stock")
    response = _get(
        f"https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en",
    )
    if response is None:
        return []
    headlines: list[NewsHeadline] = []
    for title, link, summary, published in _parse_rss_items(response.text):
        headlines.append(
            NewsHeadline(
                title=title,
                url=_unwrap_google_news_url(link),
                summary=summary,
                published_at=published,
                ticker=ticker,
                provider="google_news_rss",
            )
        )
        if len(headlines) >= limit:
            break
    return headlines


# Back-compat alias used by older call sites
def fetch_yahoo_headlines(ticker: str, limit: int = 3) -> list[NewsHeadline]:
    return fetch_latest_headlines(ticker, limit=limit)


def fetch_latest_headlines(ticker: str, limit: int = 5) -> list[NewsHeadline]:
    """
    Pull + merge + dedupe headlines for one ticker from all sources.
    """
    ticker = ticker.strip().upper()
    combined: list[NewsHeadline] = []
    combined.extend(fetch_yahoo_rss(ticker, limit=limit))
    combined.extend(fetch_yahoo_search(ticker, limit=limit))
    if len(dedupe_headlines(combined)) < max(2, limit // 2):
        combined.extend(fetch_google_news_rss(ticker, limit=limit))

    return dedupe_headlines(combined)[:limit]


def scrape_tickers(tickers: list[str], per_ticker: int = 5) -> dict[str, list[NewsHeadline]]:
    """Batch scrape for many tickers (used by the daily job)."""
    out: dict[str, list[NewsHeadline]] = {}
    for ticker in tickers:
        out[ticker.upper()] = fetch_latest_headlines(ticker, limit=per_ticker)
        time.sleep(0.35)  # be polite to public endpoints
    return out
