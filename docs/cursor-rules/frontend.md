---
description: Next.js frontend conventions for Investory
globs: frontend/**/*.{ts,tsx,js,jsx,css}
alwaysApply: false
---

# Frontend rules

## Stack

- Next.js App Router, React, TypeScript, Tailwind CSS.
- Functional components only.

## UX for beginners

- Plain language in UI copy.
- When showing financial terms, plan for inline explanation affordances (tooltips/expanders) rather than assuming knowledge.
- Never show “buy”, “sell”, or “price target” as product recommendations.

## Architecture

- Browser calls the FastAPI backend via a public API base URL from env (`NEXT_PUBLIC_API_URL` or similar).
- Keep API fetch helpers in `lib/`; keep UI in `components/` and routes in `app/`.
- Prefer server components by default; use client components when interactivity requires it.

## Quality

- Type props and API responses.
- Handle loading and error states for watchlist and briefing views.
- Do not commit `.env.local` secrets.
