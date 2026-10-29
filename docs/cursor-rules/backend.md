---
description: FastAPI and Supabase backend conventions
globs: backend/**/*.py
alwaysApply: false
---

# Backend rules

## Database

- Use the shared engine from `backend/app/database.py`.
- Session pooler: `sslmode=require`, URL-encode passwords (`quote_plus`), `NullPool`.
- Do not switch to transaction pooler (port 6543) without an ADR.

## FastAPI

- Keep route handlers thin; put business logic in services as features grow.
- Use SQLAlchemy 2.x style (`text()`, `select()`); prefer typed mappings.
- Validate inputs with Pydantic schemas before hitting the DB.
- Return JSON-serializable dicts/models; avoid leaking internal ORM state.

## Structure

```
backend/app/
  main.py
  database.py
  api/        # routers
  models/
  schemas/
  services/
  core/
```

Create these packages when adding the first real domain feature (watchlist), not before.

## Safety

- Load secrets only via env / `.env`.
- No hardcoded project refs, passwords, or API keys in source.
