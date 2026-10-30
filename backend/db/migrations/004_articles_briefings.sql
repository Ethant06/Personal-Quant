-- News + briefing persistence for demo pipeline
CREATE TABLE IF NOT EXISTS investory.articles (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    ticker       TEXT,
    title        TEXT NOT NULL,
    url          TEXT NOT NULL,
    summary      TEXT,
    published_at TIMESTAMPTZ,
    provider     TEXT NOT NULL DEFAULT 'yahoo',
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT articles_url_unique UNIQUE (url)
);

CREATE INDEX IF NOT EXISTS articles_ticker_idx ON investory.articles (ticker);
CREATE INDEX IF NOT EXISTS articles_published_at_idx ON investory.articles (published_at DESC);

CREATE TABLE IF NOT EXISTS investory.briefings (
    id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id    UUID NOT NULL REFERENCES investory.users (id) ON DELETE CASCADE,
    briefing_date DATE NOT NULL DEFAULT CURRENT_DATE,
    status     TEXT NOT NULL DEFAULT 'ready',
    note       TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT briefings_user_date_unique UNIQUE (user_id, briefing_date)
);

CREATE TABLE IF NOT EXISTS investory.briefing_items (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    briefing_id     UUID NOT NULL REFERENCES investory.briefings (id) ON DELETE CASCADE,
    article_id      UUID REFERENCES investory.articles (id) ON DELETE SET NULL,
    ticker          TEXT,
    category        TEXT NOT NULL DEFAULT 'other',
    headline        TEXT NOT NULL,
    what_happened   TEXT NOT NULL,
    why_it_matters  TEXT NOT NULL,
    macro_link      TEXT,
    terms           TEXT[] NOT NULL DEFAULT '{}',
    uncertainties   TEXT NOT NULL DEFAULT '',
    facts           TEXT[] NOT NULL DEFAULT '{}',
    implications    TEXT[] NOT NULL DEFAULT '{}',
    source_urls     TEXT[] NOT NULL DEFAULT '{}',
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX IF NOT EXISTS briefing_items_briefing_id_idx
    ON investory.briefing_items (briefing_id);
