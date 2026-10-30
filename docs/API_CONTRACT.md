# Investory API contract (1-week sprint)

All protected routes need: `Authorization: Bearer <supabase_access_token>`

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | DB + auth config check (public) |
| GET | `/auth/me` | Current Investory profile |
| GET | `/companies/search?q=` | Search local/seeded companies |
| GET | `/companies/{ticker}/hub` | Per-ticker hub (digest, articles, SEC, macro) |
| POST | `/companies` | Upsert company `{ticker,name,exchange?}` |
| GET | `/watchlist` | Watchlist + `today_item_count` / `last_briefing_at` |
| POST | `/watchlist` | Add `{company_id}` or `{ticker,name?,exchange?}` |
| DELETE | `/watchlist/{item_id}` | Remove watchlist row |
| GET | `/briefings/today?category=` | Saved daily digest (optional category filter) |
| POST | `/briefings/generate` | Manual regenerate (demo/admin; not the happy path) |
| GET | `/articles?ticker=&category=` | Stored articles (+ classification confidence) |
| GET | `/articles/{id}` | Article detail |
| GET | `/classifications/categories` | PRD category vocabulary |
| GET | `/macro/indicators` | Curated FRED series (live values need `FRED_API_KEY`) |
| POST | `/internal/jobs/news-scrape` | Scrape+store articles for watched tickers (`X-Job-Secret`) |
| POST | `/internal/jobs/daily-ingest` | Scrape + rebuild digests (`X-Job-Secret`) |

Swagger: `http://127.0.0.1:8000/docs`
