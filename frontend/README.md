# Frontend (Next.js)

This folder is reserved for the Investory Next.js app.

It is intentionally empty until Week 1 work to scaffold Next.js begins.

## Planned stack

- Next.js (App Router)
- React + TypeScript
- Tailwind CSS

## Suggested scaffold command (when starting that work)

From repo root:

```powershell
npx create-next-app@latest frontend --typescript --tailwind --eslint --app --src-dir --import-alias "@/*"
```

If `frontend/` already exists empty, scaffold in a temp folder and move files in, or remove this placeholder README first as part of that work.

## Env (later)

Create `frontend/.env.local` (never commit):

```env
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

See [../docs/REPO_STRUCTURE.md](../docs/REPO_STRUCTURE.md) and [../AGENTS.md](../AGENTS.md).
