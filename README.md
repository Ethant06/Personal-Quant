# Investory

Personalized AI financial news and education for beginner investors (college students first).

Repo name: **Personal-Quant**. Product name: **Investory**.

This app helps users follow companies on a watchlist and understand relevant company and macro developments through beginner-friendly, source-linked daily briefings. It does **not** predict prices or give buy/sell advice.

## Workspace

| Tool | Job |
|------|-----|
| Notion | Product requirements, architecture, ADRs, research, weekly notes |
| GitHub | Code, branches, commits, push, optional PRs |
| Cursor + Notion MCP | Implementation with docs context |

Details: [docs/SOURCE_OF_TRUTH.md](docs/SOURCE_OF_TRUTH.md) · Agent guide: [AGENTS.md](AGENTS.md) · Notion paste kits: [docs/notion/](docs/notion/) · Target layout: [docs/REPO_STRUCTURE.md](docs/REPO_STRUCTURE.md)

## Monorepo layout

```
backend/     FastAPI + SQLAlchemy → Supabase Postgres
frontend/    Next.js + TypeScript + Tailwind (scaffold in Week 1)
docs/        Source-of-truth notes + Notion templates
```

## Prerequisites

- Python 3.14+ (backend)
- Node.js 20+ (frontend, when scaffolded)
- Supabase project (session pooler connection)

## Backend setup

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
# or, if using the lockfile after a known-good install:
# pip install -r requirements-lock.txt
```

Create `backend/.env` (never commit):

```env
user=postgres.<project-ref>
password=<your-db-password>
host=aws-1-<region>.pooler.supabase.com
port=5432
dbname=postgres
```

Password special characters are URL-encoded in code. Use session pooler port `5432` with SQLAlchemy `NullPool`.

### Apply Week 1 schema (once)

Tables live in Postgres schema **`investory`** (same DB / same pooler URL — no `.env` change).

1. Supabase Dashboard → **SQL Editor** → run [`001_core_tables.sql`](backend/db/migrations/001_core_tables.sql)
2. Or: `python db\apply_migrations.py` from `backend/` (see [`backend/db/README.md`](backend/db/README.md))

Creates `investory.users`, `investory.companies`, `investory.watchlist_items`.

### Auth (Supabase)

1. Follow [docs/AUTH_SETUP.md](docs/AUTH_SETUP.md) (enable Email provider, copy API keys into `backend/.env`).
2. Apply [`002_auth_users_link.sql`](backend/db/migrations/002_auth_users_link.sql) (or `python db\apply_migrations.py`).
3. Sign up a user in Supabase Auth, get an access token, then call `GET /auth/me` with `Authorization: Bearer <token>`.

See [backend/.env.example](backend/.env.example) for required keys. Pooler DB URL does **not** change for Auth.

Run the API:

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload
```

- Home: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Health (DB + tables): [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Frontend setup

`frontend/` is reserved for the Next.js app. Scaffold it when you start Week 1 work (see [frontend/README.md](frontend/README.md)).

## Development workflow

1. Spec and weekly goals live in Notion.
2. Create a branch from `Main`: `feat/short-name`.
3. Commit and push as you go.
4. Open a PR when you want a clean merge history (optional); merge to `Main`.

## Six-week MVP (summary)

1. Foundation: schema, auth stub, Next.js shell  
2. Watchlist: company search + CRUD  
3. News ingest + classification  
4. Daily briefing + sources  
5. Beginner explanations + category filters  
6. Deploy (Vercel + Railway) + demo polish  

## License / disclaimer

Educational project. Not financial advice.
