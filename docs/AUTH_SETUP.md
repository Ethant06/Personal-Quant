# Investory — Supabase Auth setup (beginner guide)

## Which dashboard values to use

Supabase’s newer dashboard shows **publishable / secret** keys (not the old `anon` / `service_role` JWTs). Map them like this:

| You see in Supabase | Put in `backend/.env`? | Purpose |
|---------------------|------------------------|---------|
| **Project URL** `https://….supabase.co` | `SUPABASE_URL=…` | **Yes** |
| **Publishable key** `sb_publishable_…` | `SUPABASE_PUBLISHABLE_KEY=…` | **Yes** — public client key (like old anon) |
| **Secret key** `sb_secret_…` | **No (for now)** | Server admin key; bypasses RLS. Not needed for `/auth/me` |
| **JWKS URL** | **No (for now)** | Used for local asymmetric JWT verify later; we validate via Auth `/user` instead |
| Legacy **JWT Secret** | **No (for now)** | Old HS256 shared secret; different from `sb_secret_` |

**Important:** `SUPABASE_SECRET_KEY` ≠ JWT secret. Do not paste `sb_secret_…` into a `SUPABASE_JWT_SECRET` slot.

## Mental model

```text
Vite React app (or get_token.py)
    │  email + password
    ▼
Supabase Auth  →  auth.users  →  trigger  →  investory.users
    │
    │  access_token (user JWT)
    ▼
FastAPI  GET /auth/v1/user  (apikey = publishable, Bearer = user JWT)
    │
    ▼
GET /auth/me
```

Prefer testing via the React app at `http://localhost:5173` once the frontend is running.

## 1. Enable Email auth

1. Supabase Dashboard → **Authentication** → **Providers** → **Email** → enable  
2. For learning, you can disable **Confirm email** temporarily  

## 2. Fill `backend/.env`

```env
# existing pooler DB keys stay as-is
user=...
password=...
host=...
port=5432
dbname=postgres

SUPABASE_URL=https://YOUR_REF.supabase.co
SUPABASE_PUBLISHABLE_KEY=sb_publishable_...
```

Restart uvicorn. `GET /health` should show `"auth_configured": true`.

## 3. Migration `002` (if not already applied)

Links `investory.users` to `auth.users` and adds the signup trigger. See `backend/db/migrations/002_auth_users_link.sql`.

## 4. Create a test user

Dashboard → **Authentication** → **Users** → Add user (email + password).

## 5. Get an access token (easiest)

Create the user in Supabase Auth first, then from `backend/`:

```powershell
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
python scripts\get_token.py
```

Enter email + password when prompted. It prints an `access_token`.

Copy that token → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) → **Authorize** → paste → **GET /auth/me**.

## 6. Optional: call API from PowerShell

```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:8000/auth/me" `
  -Headers @{ Authorization = "Bearer PASTE_TOKEN_HERE" }
```


## Later (optional)

- Use **JWKS** for faster local JWT verify once you enable asymmetric signing keys  
- Use **secret key** only on trusted servers for admin/service tasks — never in the browser  
