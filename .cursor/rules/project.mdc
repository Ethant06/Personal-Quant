---
description: Investory product scope, stack, and documentation ownership
alwaysApply: true
---

# Investory — project rules

## Product

- Personalized AI financial briefings for beginner investors.
- Explain what happened, why it may matter, macro links, terms, uncertainty, and sources.
- Never add price prediction, buy/sell advice, or brokerage/trading features.

## Stack

- `backend/`: FastAPI + SQLAlchemy + Supabase Postgres (session pooler)
- `frontend/`: Next.js + TypeScript + Tailwind
- Docs narrative: Notion. Code: this repo via normal git.

## Notion scope (required)

- Product docs live **only** under the Investory parent page:  
  https://app.notion.com/p/Investory-4086257be62f809baff1fdac8c9464bd
- When using Notion MCP, search/read under that page (Overview, PRD, Architecture, ADRs, Research, Weekly notes, Glossary).
- Do **not** use other Notion pages or workspaces for this repo.

## Agent behavior

- Implement from the Notion PRD/ADR scope for the current session; do not expand scope.
- Prefer Notion (MCP) over inventing requirements.
- Never commit `.env` or secrets; never print DB passwords.
- Prefer small commits on a feature branch; push regularly.
- If an architecture decision changes, note that a Notion ADR update is required.

## Monorepo

- Do not dump unrelated packages at repo root.
- Grow `backend/app/{api,models,schemas,services}` only when needed.
- Frontend lives only under `frontend/`.
