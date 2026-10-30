-- Epic B: category on articles + classifications metadata
ALTER TABLE investory.articles
    ADD COLUMN IF NOT EXISTS category TEXT NOT NULL DEFAULT 'other';

ALTER TABLE investory.articles
    ADD COLUMN IF NOT EXISTS title_norm TEXT;

CREATE INDEX IF NOT EXISTS articles_category_idx ON investory.articles (category);
CREATE INDEX IF NOT EXISTS articles_title_norm_idx ON investory.articles (title_norm);

CREATE TABLE IF NOT EXISTS investory.classifications (
    id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    article_id   UUID NOT NULL REFERENCES investory.articles (id) ON DELETE CASCADE,
    category     TEXT NOT NULL,
    confidence   DOUBLE PRECISION NOT NULL DEFAULT 0.5,
    model        TEXT NOT NULL DEFAULT 'heuristic_v1',
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT classifications_article_unique UNIQUE (article_id)
);

CREATE INDEX IF NOT EXISTS classifications_category_idx
    ON investory.classifications (category);
