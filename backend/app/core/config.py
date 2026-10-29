"""
Load settings from backend/.env once for the whole app.

Why this file exists: uvicorn / scripts may start with different working
directories. Loading via Path(__file__) always finds backend/.env.
"""
from pathlib import Path

from dotenv import load_dotenv
import os

# parents[0]=core, [1]=app, [2]=backend
_BACKEND_DIR = Path(__file__).resolve().parents[2]
load_dotenv(_BACKEND_DIR / ".env", encoding="utf-8")


# --- Database (Supabase session pooler connection string pieces) ---
DB_USER = os.getenv("user")
DB_PASSWORD = os.getenv("password")
DB_HOST = os.getenv("host")
DB_PORT = os.getenv("port")
DB_NAME = os.getenv("dbname")

# Postgres schema that owns Investory tables (not the same as "database name")
APP_SCHEMA = "investory"

# --- Supabase Auth / HTTP API ---
# Project URL + publishable key (sb_publishable_...). Used to call Auth endpoints.
# Do NOT put sb_secret_... here for login verification — that is an admin key.
SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip("/")
SUPABASE_PUBLISHABLE_KEY = (
    os.getenv("SUPABASE_PUBLISHABLE_KEY")
    or os.getenv("SUPABASE_ANON_KEY")  # legacy name, if you still have it
    or ""
)


def db_env_ready() -> bool:
    return all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME])


def auth_env_ready() -> bool:
    """True when FastAPI can verify user tokens via Supabase Auth /user."""
    return bool(SUPABASE_URL and SUPABASE_PUBLISHABLE_KEY)
