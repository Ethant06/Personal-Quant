from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
import os

# Load environment variables from backend/.env
load_dotenv()

USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
DBNAME = os.getenv("dbname")

if not all([USER, PASSWORD, HOST, PORT, DBNAME]):
    raise RuntimeError(
        "Missing database env vars. Expected user, password, host, port, dbname in backend/.env"
    )

# Special characters in the password (e.g. @) must be URL-encoded
DATABASE_URL = (
    f"postgresql+psycopg2://{USER}:{quote_plus(PASSWORD)}"
    f"@{HOST}:{PORT}/{DBNAME}?sslmode=require"
)

# Session/Transaction pooler: disable SQLAlchemy's client-side pool so
# Supabase's pooler owns connection lifecycle.
# https://docs.sqlalchemy.org/en/20/core/pooling.html#switching-pool-implementations
engine = create_engine(DATABASE_URL, poolclass=NullPool)
