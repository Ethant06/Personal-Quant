import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import { getTodayBriefing, type Briefing } from '../lib/api'

export function BriefingPage() {
  const { accessToken } = useAuth()
  const [briefing, setBriefing] = useState<Briefing | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!accessToken) return
    void getTodayBriefing(accessToken)
      .then(setBriefing)
      .catch((err) =>
        setError(err instanceof Error ? err.message : 'Failed to load briefing'),
      )
  }, [accessToken])

  return (
    <main className="page wide">
      <header className="header">
        <div>
          <h1>All updates</h1>
          <p className="muted">
            Combined daily digest across your watchlist. Open a ticker card for the full
            company hub. Not investment advice.
          </p>
        </div>
      </header>

      {error && <p className="error">{error}</p>}
      {briefing?.note && <p className="info">{briefing.note}</p>}

      {!briefing || briefing.items.length === 0 ? (
        <section className="card">
          <p className="muted">
            No digest items yet. Add watchlist companies — the daily job fills this
            automatically.
          </p>
          <p>
            <Link to="/watchlist">Go to watchlist</Link>
          </p>
        </section>
      ) : (
        <div className="stack">
          {briefing.items.map((item) => (
            <article key={item.id} className="card briefing-card">
              <p className="eyebrow">
                {item.ticker ? (
                  <Link to={`/companies/${item.ticker}`}>{item.ticker}</Link>
                ) : (
                  'Market'
                )}{' '}
                · {item.category}
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
          ))}
        </div>
      )}
    </main>
  )
}
