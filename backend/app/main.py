"""
FastAPI entrypoint.

Keep this file thin: create the app, mount routers, expose / and /health.
Domain endpoints belong in app/api/*.py
"""
from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from app.api.auth import router as auth_router
from app.core.config import APP_SCHEMA, auth_env_ready
from app.database import engine

app = FastAPI(title="Investory API", version="0.1.0")

# Registers routes from app/api/auth.py (e.g. GET /auth/me)
app.include_router(auth_router)

CORE_TABLES = ("users", "companies", "watchlist_items")


@app.get("/")
def home():
    return {
        "message": "Investory API is running",
        "product": "Investory",
        "auth_configured": auth_env_ready(),
    }


@app.get("/health")
def health():
    """
    Ops check: can we reach Postgres, and do core investory.* tables exist?
    Useful after migrations and for deploy health checks later.
    """
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            rows = connection.execute(
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
            found = {row[0] for row in rows}
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={"status": "error", "database": "unreachable", "error": str(exc)},
        ) from exc

    missing = sorted(set(CORE_TABLES) - found)
    if missing:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "degraded",
                "database": "connected",
                "schema": APP_SCHEMA,
                "missing_tables": missing,
                "hint": "Apply backend/db/migrations/001_core_tables.sql",
            },
        )

    return {
        "status": "ok",
        "database": "connected",
        "schema": APP_SCHEMA,
        "tables": sorted(found),
        "auth_configured": auth_env_ready(),
    }
