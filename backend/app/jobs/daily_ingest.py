"""
Run from backend/ with PYTHONPATH set:

  python -m app.jobs.daily_ingest
"""
from app.services.daily_ingest import run_daily_ingest


def main() -> None:
    summary = run_daily_ingest()
    print(summary)


if __name__ == "__main__":
    main()
