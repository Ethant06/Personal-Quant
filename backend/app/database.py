"""
SQLAlchemy engine for Investory.

We talk to Supabase Postgres through the *session pooler* (IPv4-friendly).
App tables live in schema `investory` inside database `postgres` — the
connection URL does NOT change when you add a schema.
"""
from urllib.parse import quote_plus

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from app.core.config import (
    APP_SCHEMA,
    DB_HOST,
    DB_NAME,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
    db_env_ready,
)

if not db_env_ready():
    raise RuntimeError(
        "Missing database env vars. Expected user, password, host, port, dbname in backend/.env"
    )

# quote_plus: passwords may contain @, !, etc. Without encoding, those break the URL
# (Postgres would think the host starts after the first @).
DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{quote_plus(DB_PASSWORD)}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}?sslmode=require"
)

# NullPool: do not keep a client-side connection pool. Supabase's pooler already
# pools connections; stacking two pools can exhaust limits.
#
# search_path: unqualified names like "users" resolve to investory.users first,
# then public. Other schemas (auth, storage) are still reachable as auth.users, etc.
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,
    connect_args={"options": f"-csearch_path={APP_SCHEMA},public"},
)
