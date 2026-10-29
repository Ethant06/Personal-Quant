# Target repository structure

This is the intended monorepo shape for Investory. Build folders as Week 1–2 work requires — do not invent empty package trees ahead of need.

```
Personal-Quant/
├── AGENTS.md
├── README.md
├── .gitignore
├── .cursor/
│   └── rules/
│       ├── project.mdc      # always on
│       ├── backend.mdc      # backend/**/*.py
│       └── frontend.mdc     # frontend/**/*.{ts,tsx}
├── .github/
│   ├── ISSUE_TEMPLATE/      # optional
│   │   ├── feature.md
│   │   └── bug.md
│   └── PULL_REQUEST_TEMPLATE.md
├── docs/
│   ├── SOURCE_OF_TRUTH.md
│   ├── REPO_STRUCTURE.md
│   ├── cursor-rules/        # copy into .cursor/rules as .mdc
│   └── notion/              # paste into Notion
│       ├── 00_OVERVIEW.md
│       ├── 01_PRD.md
│       ├── 02_ARCHITECTURE.md
│       ├── 03_ADRS.md
│       ├── 04_RESEARCH.md
│       ├── 05_WEEKLY_NOTES.md
│       ├── 06_GLOSSARY.md
│       └── SETUP.md
├── backend/
│   ├── .env                 # local only
│   ├── requirements.txt
│   ├── requirements-lock.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py          # FastAPI entry
│       ├── database.py      # Supabase engine
│       ├── api/             # routers (add when endpoints grow)
│       ├── models/          # SQLAlchemy / Pydantic models
│       ├── schemas/         # request/response schemas
│       ├── services/        # business logic, LLM, ingest
│       └── core/            # config, security helpers
└── frontend/                # Next.js App Router (Week 1 scaffold)
    ├── package.json
    ├── src/ or app/
    ├── components/
    ├── lib/                 # API client, utils
    └── public/
```

## Growth rules

1. **Backend:** start flat (`main.py` + `database.py`). When you add a third feature area, introduce `api/`, `models/`, `schemas/`, `services/`.
2. **Frontend:** scaffold with `create-next-app` once; keep routes under App Router (`app/`).
3. **Shared types:** prefer OpenAPI-generated client later; do not create a premature `packages/` monorepo workspace in MVP.
4. **Migrations:** add Alembic (or Supabase SQL migrations) when the first real schema ships — Week 1.

## Data domains (logical, not folders yet)

| Domain | Examples |
|--------|----------|
| Identity | users, sessions (Supabase Auth later) |
| Watchlist | companies, user_watchlist |
| Ingest | raw_articles, article_company_links |
| Intelligence | classifications, briefings, briefing_items |
| Education | term glossary links inside briefing items |
