# Database migrations

App tables live in Postgres schema **`investory`** inside the Supabase database `postgres`.

The session pooler / `.env` URL does **not** change for a schema. You still connect to `dbname=postgres`.

## Apply

### Option A — Supabase SQL Editor

Run [`migrations/001_core_tables.sql`](migrations/001_core_tables.sql).

### Option B — local helper

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = (Get-Location).Path
python db\apply_migrations.py
```

### Verify

`GET http://127.0.0.1:8000/health` → `"status": "ok"`, `"schema": "investory"`.

## Migrations

| File | Purpose |
|------|---------|
| `001_core_tables.sql` | Schema `investory` + users / companies / watchlist_items |
| `002_auth_users_link.sql` | Minimal Auth link: drop id default, FK to `auth.users`, signup trigger |

`002` is one-shot (apply once). Auth setup walkthrough: [../../docs/AUTH_SETUP.md](../../docs/AUTH_SETUP.md).

## Tables

- `investory.users` (id = `auth.users.id`)
- `investory.companies`
- `investory.watchlist_items`
