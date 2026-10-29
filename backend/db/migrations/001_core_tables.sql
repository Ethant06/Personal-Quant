-- Investory — core tables (schema: investory)
-- Apply via Supabase SQL Editor or: python db/apply_migrations.py
-- Pooler URL unchanged (dbname=postgres). Safe to re-run (IF NOT EXISTS).

-- Needed for gen_random_uuid() on older Postgres; no-op if already installed
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- Namespace for app tables (keeps them separate from public / auth / storage)
CREATE SCHEMA IF NOT EXISTS investory;

-- ---------------------------------------------------------------------------
-- users = application *profile* (not passwords — Auth owns that in auth.users)
-- After migration 002, id must equal auth.users.id (same UUID).
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS investory.users (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email        TEXT UNIQUE,
    display_name TEXT,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at   TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS users_email_idx ON investory.users (email);

-- ---------------------------------------------------------------------------
-- companies = tickers users can follow
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS investory.companies (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker     TEXT NOT NULL,
    name       TEXT NOT NULL,
    exchange   TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT companies_ticker_unique UNIQUE (ticker)
);

CREATE INDEX IF NOT EXISTS companies_ticker_idx ON investory.companies (ticker);
CREATE INDEX IF NOT EXISTS companies_name_idx ON investory.companies (name);

-- ---------------------------------------------------------------------------
-- watchlist_items = which companies each user follows (many-to-many)
-- ON DELETE CASCADE: remove watchlist rows if user or company is deleted
-- UNIQUE(user_id, company_id): cannot follow the same company twice
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS investory.watchlist_items (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id    UUID NOT NULL REFERENCES investory.users (id) ON DELETE CASCADE,
    company_id UUID NOT NULL REFERENCES investory.companies (id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT watchlist_items_user_company_unique UNIQUE (user_id, company_id)
);

CREATE INDEX IF NOT EXISTS watchlist_items_user_id_idx
    ON investory.watchlist_items (user_id);

CREATE INDEX IF NOT EXISTS watchlist_items_company_id_idx
    ON investory.watchlist_items (company_id);

-- ---------------------------------------------------------------------------
-- Trigger: keep updated_at current on UPDATE
-- ---------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION investory.set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS users_set_updated_at ON investory.users;
CREATE TRIGGER users_set_updated_at
    BEFORE UPDATE ON investory.users
    FOR EACH ROW
    EXECUTE PROCEDURE investory.set_updated_at();

DROP TRIGGER IF EXISTS companies_set_updated_at ON investory.companies;
CREATE TRIGGER companies_set_updated_at
    BEFORE UPDATE ON investory.companies
    FOR EACH ROW
    EXECUTE PROCEDURE investory.set_updated_at();
