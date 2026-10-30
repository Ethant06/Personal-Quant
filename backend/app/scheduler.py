"""
In-process daily news scrape scheduler.

When ENABLE_DAILY_SCHEDULER=true, a background thread wakes once per day at
DAILY_INGEST_HOUR_UTC (default 13:00 UTC ≈ morning US market hours).

Production can also use Railway/cron → POST /internal/jobs/daily-ingest.
"""
from __future__ import annotations

import logging
import threading
import time
from datetime import datetime, timedelta, timezone

from app.core.config import DAILY_INGEST_HOUR_UTC, ENABLE_DAILY_SCHEDULER
from app.services.daily_ingest import run_daily_ingest

logger = logging.getLogger(__name__)

_stop = threading.Event()
_thread: threading.Thread | None = None


def _seconds_until_next_run(hour_utc: int) -> float:
    now = datetime.now(timezone.utc)
    target = now.replace(hour=hour_utc, minute=0, second=0, microsecond=0)
    if target <= now:
        target = target + timedelta(days=1)
    return max(5.0, (target - now).total_seconds())


def _loop() -> None:
    logger.info(
        "Daily news scheduler enabled (hour_utc=%s)",
        DAILY_INGEST_HOUR_UTC,
    )
    while not _stop.is_set():
        wait_s = _seconds_until_next_run(DAILY_INGEST_HOUR_UTC)
        logger.info("Next daily news scrape in %.0f seconds", wait_s)
        if _stop.wait(timeout=wait_s):
            break
        try:
            summary = run_daily_ingest()
            logger.info("Daily news scrape finished: %s", summary)
        except Exception:
            logger.exception("Daily news scrape failed")


def start_scheduler() -> None:
    global _thread
    if not ENABLE_DAILY_SCHEDULER:
        logger.info("Daily news scheduler disabled (set ENABLE_DAILY_SCHEDULER=true)")
        return
    if _thread and _thread.is_alive():
        return
    _stop.clear()
    _thread = threading.Thread(target=_loop, name="investory-daily-ingest", daemon=True)
    _thread.start()


def stop_scheduler() -> None:
    _stop.set()
