# Investory frontend (Vite + React)

## Setup

```powershell
npm install
# copy .env.example → .env and fill values
npm run dev
```

## Env (`frontend/.env`)

```env
VITE_SUPABASE_URL=https://YOUR_PROJECT.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=sb_publishable_...
VITE_API_URL=http://127.0.0.1:8000
```

## What works today

- Sign up / sign in via Supabase Auth
- After login, loads profile from FastAPI `GET /auth/me`

Run the backend at the same time (`uvicorn app.main:app --reload` in `backend/`).
