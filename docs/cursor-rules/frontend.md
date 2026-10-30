---
description: Vite React frontend conventions for Investory
globs: frontend/**/*.{ts,tsx,js,jsx,css}
alwaysApply: false
---

# Frontend rules

## Stack

- Vite + React + TypeScript (SPA). Not Next.js.
- Functional components only.

## UX for beginners

- Plain language in UI copy.
- When showing financial terms, plan for inline explanation affordances (tooltips/expanders) rather than assuming knowledge.
- Never show “buy”, “sell”, or “price target” as product recommendations.

## Architecture

- Auth: `@supabase/supabase-js` in the browser.
- API: call FastAPI via `import.meta.env.VITE_API_URL` with `Authorization: Bearer <access_token>`.
- Keep clients in `src/lib/`; keep UI in `src/` components / pages as the app grows.

## Quality

- Type props and API responses.
- Handle loading and error states for auth, watchlist, and briefing views.
- Do not commit `frontend/.env`.
