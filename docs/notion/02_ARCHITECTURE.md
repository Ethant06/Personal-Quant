# Investory — Architecture

Status: Living doc for MVP  
Related ADRs: [[03 — ADRs]]

## High-level diagram

```text
[Next.js / Vercel]  --HTTPS JSON-->  [FastAPI / Railway]
                                          |
                                          v
                               [Supabase Postgres]
                               (Session pooler :5432)
                                          ^
                                          |
                    [Ingest workers / scheduled jobs]
                     | news API | SEC EDGAR | FRED |
                                          |
                                          v
                                    [LLM provider]
                         classify / summarize / explain
```

## Components

| Component | Responsibility |
|-----------|----------------|
| Frontend | Auth UI, watchlist UX, briefing reader, term explainers |
| Backend API | CRUD, briefing fetch, admin/trigger endpoints |
| Database | Users, companies, watchlists, articles, classifications, briefings |
| Ingest | Pull + normalize + dedupe external content |
| AI layer | Classify, summarize, beginner explanations, uncertainty tags |
| Auth | Supabase Auth preferred for MVP (ADR) |

## Core data model (logical)

- **users** — identity
- **companies** — ticker, name, exchange metadata
- **watchlist_items** — user_id + company_id
- **articles** — title, url, published_at, raw text/summary, provider id
- **article_companies** — many-to-many
- **classifications** — category, confidence, model meta
- **briefings** — user_id, date, status
- **briefing_items** — briefing_id, article_id, what/why/macro/terms/uncertainty/fact_vs_implication

Exact SQL lands in Week 1; update this page when schema is committed.

## Request flows

### Add to watchlist

1. UI search → `GET /companies/search?q=`
2. UI add → `POST /watchlist`
3. Persist `watchlist_items`

### Generate / view briefing

1. Scheduler or `POST /briefings/generate`
2. Select recent classified articles for user’s tickers
3. LLM produces structured briefing items (JSON schema)
4. Persist + `GET /briefings/today`

## AI constraints

- Structured output only (JSON schema / tool calling)
- Prompt includes non-goals: no price targets, no buy/sell
- Every item must keep `source_urls[]`
- Separate fields: `facts`, `implications`, `uncertainties`

## Environments

| Env | Frontend | Backend | DB |
|-----|----------|---------|----|
| Local | localhost:3000 | localhost:8000 | Supabase pooler |
| Prod | Vercel | Railway | Supabase pooler |

## Open questions

- News provider choice (Research page)
- Auth: Supabase Auth vs deferred demo user (ADR)
- Briefing generation: cron on Railway vs manual button for MVP
