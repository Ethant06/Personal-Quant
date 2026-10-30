import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import { getCompanyHub, type BriefingItem, type CompanyHub } from '../lib/api'

function ExplainCard({ item }: { item: BriefingItem }) {
  return (
    <article className="card briefing-card">
      <p className="eyebrow">
        {item.ticker ?? 'Market'} · {item.category}
      </p>
      <h2>{item.headline}</h2>
      <section>
        <h3>What happened</h3>
        <p>{item.what_happened}</p>
      </section>
      <section>
        <h3>Why it may matter</h3>
        <p>{item.why_it_matters}</p>
      </section>
      {item.macro_link && (
        <section>
          <h3>Macro / bigger picture</h3>
          <p>{item.macro_link}</p>
        </section>
      )}
      <section>
        <h3>What is uncertain</h3>
        <p>{item.uncertainties}</p>
      </section>
      {item.source_urls.length > 0 && (
        <p>
          Sources:{' '}
          {item.source_urls.map((url) => (
            <a key={url} href={url} target="_blank" rel="noreferrer">
              {url}
            </a>
          ))}
        </p>
      )}
    </article>
  )
}

export function CompanyHubPage() {
  const { ticker = '' } = useParams()
  const { accessToken } = useAuth()
  const [hub, setHub] = useState<CompanyHub | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!accessToken || !ticker) return
    void getCompanyHub(accessToken, ticker)
      .then(setHub)
      .catch((err) =>
        setError(err instanceof Error ? err.message : 'Failed to load company hub'),
      )
  }, [accessToken, ticker])

  if (error) {
    return (
      <main className="page wide">
        <p className="error">{error}</p>
        <Link to="/watchlist">Back to watchlist</Link>
      </main>
    )
  }

  if (!hub) {
    return (
      <main className="page wide">
        <p className="muted">Loading hub…</p>
      </main>
    )
  }

  return (
    <main className="page wide">
      <p className="back">
        <Link to="/watchlist">← Watchlist</Link>
      </p>
      <header className="header">
        <div>
          <p className="eyebrow">{hub.company.exchange ?? 'Company hub'}</p>
          <h1>
            {hub.company.ticker}{' '}
            <span className="hub-name">{hub.company.name}</span>
          </h1>
          <p className="muted">
            Educational overview from news, filings, and macro context. Not investment
            advice.
          </p>
        </div>
      </header>

      {hub.note && <p className="info">{hub.note}</p>}

      <section className="hub-section">
        <h2>Today’s explainers</h2>
        {hub.items.length === 0 ? (
          <div className="card">
            <p className="muted">
              No digest items yet for this ticker. They appear after the daily refresh.
            </p>
          </div>
        ) : (
          <div className="stack">
            {hub.items.map((item) => (
              <ExplainCard key={item.id} item={item} />
            ))}
          </div>
        )}
      </section>

      <section className="hub-section">
        <h2>Yahoo / news articles</h2>
        {hub.articles.length === 0 ? (
          <div className="card">
            <p className="muted">No stored articles yet.</p>
          </div>
        ) : (
          <ul className="hub-list">
            {hub.articles.map((article) => (
              <li key={article.id} className="card">
                <p className="eyebrow">{article.provider}</p>
                <a href={article.url} target="_blank" rel="noreferrer">
                  {article.title}
                </a>
                {article.summary && <p className="muted">{article.summary}</p>}
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="hub-section">
        <h2>SEC filings</h2>
        {hub.filings.length === 0 ? (
          <div className="card">
            <p className="muted">
              No recent 8-K / 10-Q / 10-K filings found (or SEC was unreachable).
            </p>
          </div>
        ) : (
          <ul className="hub-list">
            {hub.filings.map((filing) => (
              <li key={filing.url} className="card">
                <p className="eyebrow">
                  {filing.form}
                  {filing.filed_at ? ` · ${filing.filed_at}` : ''}
                </p>
                <a href={filing.url} target="_blank" rel="noreferrer">
                  {filing.title}
                </a>
              </li>
            ))}
          </ul>
        )}
      </section>

      <section className="hub-section">
        <h2>Macro & politics context</h2>
        <p className="muted section-lead">
          Broader themes (energy, rates, geopolitics) that may relate to companies you
          follow — read sources and decide what connects.
        </p>
        <ul className="hub-list">
          {hub.macro_signals.map((signal) => (
            <li key={`${signal.theme}-${signal.headline}`} className="card">
              <p className="eyebrow">{signal.theme.replaceAll('_', ' ')}</p>
              <h3 className="hub-signal-title">{signal.headline}</h3>
              <p>{signal.why_it_may_matter}</p>
              {signal.source_url && (
                <p>
                  <a href={signal.source_url} target="_blank" rel="noreferrer">
                    Source
                  </a>
                </p>
              )}
            </li>
          ))}
        </ul>
      </section>
    </main>
  )
}
