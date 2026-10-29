"""
Apply every *.sql file in db/migrations/ in sorted filename order.

MVP approach: plain SQL files + this script (or Supabase SQL Editor).
Later you might switch to Alembic; same idea — versioned schema changes.

Run from backend/:
  export PYTHONPATH=.
  python db/apply_migrations.py
"""
from pathlib import Path

from sqlalchemy import text

from app.core.config import APP_SCHEMA
from app.database import engine

MIGRATIONS_DIR = Path(__file__).resolve().parent / "migrations"


def main() -> None:
    # Sorted so 001_ runs before 002_
    files = sorted(MIGRATIONS_DIR.glob("*.sql"))
    if not files:
        raise SystemExit(f"No .sql files in {MIGRATIONS_DIR}")

    for path in files:
        sql = path.read_text(encoding="utf-8")
        # begin() = one transaction per file; commit on success, rollback on error
        with engine.begin() as conn:
            conn.execute(text(sql))
        print(f"Applied {path.name}")

    # Quick sanity check that core tables exist in schema investory
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = :schema
                  AND table_name IN ('users', 'companies', 'watchlist_items')
                ORDER BY table_name
                """
            ),
            {"schema": APP_SCHEMA},
        ).fetchall()
    print(f"schema={APP_SCHEMA} tables:", [r[0] for r in rows])


if __name__ == "__main__":
    main()
