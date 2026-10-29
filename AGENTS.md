# AGENTS.md — Investory

Operating guide for humans and AI agents working in this repo.

## Product

**Investory** (repo: Personal-Quant) is a personalized AI financial news and education app for college students and beginner investors.

Users maintain a company watchlist and receive daily briefings that explain what happened, why it may matter, how macro events connect, what terms mean, what is uncertain, and where to read sources.

### Non-goals (never implement)

- Stock price prediction
- Buy / sell / hold recommendations
- Portfolio brokerage or order execution

## Stack

| Layer | Choice |
|-------|--------|
| Frontend | Next.js, React, TypeScript, Tailwind (`frontend/`) |
| Backend | Python, FastAPI (`backend/`) |
| Database | Supabase PostgreSQL (session pooler) |
| AI | LLM classification, summarization, beginner explanations |
| Data | Financial news provider, SEC EDGAR, FRED |
| Deploy | Vercel (frontend), Railway (backend) |

## Repo map

```
Personal-Quant/
  AGENTS.md                 # this file
  README.md                 # run instructions
  docs/                     # lightweight repo docs + Notion paste templates
  docs/cursor-rules/        # rule source files (copy to .cursor/rules as .mdc)
  .cursor/rules/            # Cursor rule packs (.mdc), once installed
  .github/                  # optional issue + PR templates
  backend/                  # FastAPI API
  frontend/                 # Next.js app (scaffold in Week 1)
```

## Source of truth

| Concern | Location |
|---------|----------|
| Product requirements, ADRs, research, weekly notes | **Notion** (Investory parent page only) |
| Code | **This repo** (git branches, commits, push) |

**Canonical Notion parent (use only this tree):**  
https://app.notion.com/p/Investory-4086257be62f809baff1fdac8c9464bd

Child pages under it: Overview, PRD, Architecture, ADRs, Research, Weekly notes, Glossary.

Full ownership rules: [docs/SOURCE_OF_TRUTH.md](docs/SOURCE_OF_TRUTH.md).  
Notion page paste kits: [docs/notion/](docs/notion/).

Before implementing a feature: read the matching Notion PRD/ADR under that parent (via Notion MCP). Ignore other Notion pages/workspaces. Do not invent product scope that contradicts Notion.

## Backend conventions

- Env vars live in `backend/.env` (never commit). Keys today: `user`, `password`, `host`, `port`, `dbname`.
- DB engine: SQLAlchemy + Supabase **session pooler**, `sslmode=require`, URL-encode passwords, `NullPool` (see `backend/app/database.py`).
- Prefer small FastAPI routers under `backend/app/` as the API grows (`api/`, `models/`, `services/`).
- No raw SQL scattered in route handlers long-term — keep queries near models/services.

## Frontend conventions

- App Router + TypeScript strict.
- Talk to the FastAPI backend via env-based API base URL.
- Keep UI beginner-friendly; no trading jargon without explanation affordances.

## Git workflow (manual)

Keep it simple — no project boards.

1. Pull latest `Main`.
2. Branch: `feat/short-name` (or `fix/` / `chore/`).
3. Implement only the scoped change from Notion for that session.
4. Commit with a clear message; push the branch.
5. Open a PR when you want review history (optional but good practice); merge to `Main`.
6. If architecture changed, add/update a Notion ADR.

## Definition of Done

- Scoped change from Notion is complete
- Changes committed (and pushed)
- Secrets not committed
- README updated if run steps changed
- Notion ADR updated when architecture decisions change

## Security

- Never commit `.env`, API keys, or tokens
- Never log passwords or full connection strings
- Rotate credentials if they appear in chat or screenshots
