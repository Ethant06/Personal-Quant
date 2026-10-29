# Investory — PRD (MVP)

Status: Draft for six-week MVP  
Last updated: 2026-10-29

## Goals

1. User can search public companies and maintain a personal watchlist.
2. System produces a daily AI briefing tailored to that watchlist.
3. Briefings classify news, explain beginner terms, and link to sources.
4. Product remains educational — never trade advice.

## Out of scope (MVP)

Email/push delivery, custom briefing frequency, fundamentals dashboards, quizzes, historical journals, interactive macro diagrams.

---

## Epic A — Watchlist

**User story:** As a beginner investor, I want to follow companies I care about so briefings stay relevant.

### Acceptance criteria

- [ ] Search publicly traded companies by name or ticker
- [ ] Add / remove companies on my watchlist
- [ ] See my current watchlist after refresh
- [ ] Empty state explains how to add the first company

**Target week:** 2

---

## Epic B — Ingest and classification

**User story:** As a user, I want relevant developments gathered and organized so I am not reading duplicate headlines.

### Categories (MVP)

Earnings, partnerships, acquisitions, product innovation, competition, government policy, inflation, interest rates, other/macro.

### Acceptance criteria

- [ ] Ingest articles/events from at least one news source (plus stub hooks for SEC/FRED later)
- [ ] Deduplicate near-identical items
- [ ] Assign primary category + related tickers/companies
- [ ] Store source URL and published time

**Target week:** 3

---

## Epic C — Daily AI briefing

**User story:** As a student, I want a short daily digest for my watchlist so I can stay informed without deep research time.

### Each briefing item must include

1. What happened (plain language)
2. Why it may matter to the company
3. Macro / political connection when relevant
4. Beginner term callouts
5. Uncertainty / what we do not know
6. Link(s) to original source(s)
7. Clear labeling: **Fact** vs **Possible implication** vs **Uncertainty**

### Acceptance criteria

- [ ] Generate one briefing per user per day (batch job or on-demand MVP button is OK)
- [ ] Only include items tied to the user’s watchlist (or clearly marked macro affecting those names)
- [ ] Every item has at least one source link
- [ ] No buy/sell language in model output (prompt + light post-check)

**Target week:** 4

---

## Epic D — Beginner education layer

**User story:** As a beginner, I want terms explained in context of companies I follow.

### Acceptance criteria

- [ ] Key terms in a briefing are highlighted or expandable
- [ ] Definitions use accessible language + one contextual example
- [ ] Glossary can grow over time (see Glossary page)

**Target week:** 5

---

## Epic E — Platform foundation

### Acceptance criteria

- [ ] Supabase Postgres connected; core tables exist
- [ ] FastAPI serves health + domain APIs
- [ ] Next.js UI shell with navigation to Watchlist and Briefing
- [ ] Auth stub or real auth sufficient for one-user-per-session demo
- [ ] Deployed: frontend on Vercel, backend on Railway

**Target week:** 1 (foundation) + 6 (deploy)

---

## Success metrics (qualitative for class demo)

- Demo user can add 3 companies and open a briefing in under 2 minutes
- A non-finance classmate understands one briefing item without extra explanation
- Every claim in the demo briefing has a visible source link

## Risks

| Risk | Mitigation |
|------|------------|
| News API cost / rate limits | Start with one provider; cache; limit universe |
| LLM hallucinations | Require sources; separate fact vs implication |
| Scope creep into “trading app” | Enforce non-goals in AGENTS.md + Notion |
