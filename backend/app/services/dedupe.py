"""
Near-duplicate headline detection for ingest (PRD Epic B).
"""
from __future__ import annotations

from typing import Protocol, TypeVar

from app.services.classify import normalize_text


class _HasTitleUrl(Protocol):
    title: str
    url: str


T = TypeVar("T", bound=_HasTitleUrl)


def _tokens(text: str) -> set[str]:
    return {t for t in normalize_text(text).split() if len(t) > 2}


def is_near_duplicate(a: str, b: str, threshold: float = 0.72) -> bool:
    ta, tb = _tokens(a), _tokens(b)
    if not ta or not tb:
        return normalize_text(a) == normalize_text(b)
    overlap = len(ta & tb) / max(1, len(ta | tb))
    return overlap >= threshold


def dedupe_headlines(headlines: list[T]) -> list[T]:
    """Keep first occurrence; drop near-identical titles / same URL."""
    kept: list[T] = []
    for h in headlines:
        if any(h.url == k.url for k in kept):
            continue
        if any(is_near_duplicate(h.title, k.title) for k in kept):
            continue
        kept.append(h)
    return kept
