"""
Light post-checks so educational copy does not sound like trade advice.
"""
from __future__ import annotations

import re

_BANNED = re.compile(
    r"\b("
    r"buy\s+now|sell\s+now|strong\s+buy|strong\s+sell|"
    r"guaranteed\s+returns?|price\s+target|must\s+buy|must\s+sell|"
    r"you\s+should\s+(buy|sell)|definitely\s+(buy|sell)"
    r")\b",
    re.IGNORECASE,
)


def strip_advice_language(text: str) -> str:
    """Replace obvious advice phrases; keep the rest intact."""
    if not text:
        return text
    cleaned = _BANNED.sub("[educational note removed]", text)
    return cleaned
