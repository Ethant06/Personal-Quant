import { useEffect, useState, type FormEvent } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import {
  addToWatchlist,
  listWatchlist,
  removeFromWatchlist,
  searchCompanies,
  type Company,
  type WatchlistItem,
} from '../lib/api'

export function WatchlistPage() {
  const { accessToken } = useAuth()
  const [items, setItems] = useState<WatchlistItem[]>([])
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<Company[]>([])
  const [error, setError] = useState<string | null>(null)
  const [busy, setBusy] = useState(false)

  async function refresh(token: string) {
    const data = await listWatchlist(token)
    setItems(data)
  }

  useEffect(() => {
    if (!accessToken) return
    void refresh(accessToken).catch((err) =>
      setError(err instanceof Error ? err.message : 'Failed to load watchlist'),
    )
  }, [accessToken])

  async function onSearch(event: FormEvent) {
    event.preventDefault()
    if (!accessToken || !query.trim()) return
    setBusy(true)
    setError(null)
    try {
      const found = await searchCompanies(accessToken, query.trim())
      setResults(found)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Search failed')
    } finally {
      setBusy(false)
    }
  }

  async function onAdd(company: Company) {
    if (!accessToken) return
    setBusy(true)
    setError(null)
    try {
      await addToWatchlist(accessToken, { company_id: company.id })
      await refresh(accessToken)
      setResults((prev) => prev.filter((c) => c.id !== company.id))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not add company')
    } finally {
      setBusy(false)
    }
  }

  async function onRemove(itemId: string) {
    if (!accessToken) return
    setBusy(true)
    setError(null)
    try {
      await removeFromWatchlist(accessToken, itemId)
      setItems((prev) => prev.filter((item) => item.id !== itemId))
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not remove company')
    } finally {
      setBusy(false)
    }
  }

  const lastRefresh = items.find((i) => i.last_briefing_at)?.last_briefing_at

  return (
    <main className="page wide">
      <header className="header">
        <div>
          <h1>Watchlist</h1>
          <p className="muted">
            Open a company card for today’s news, filings, and macro context. Digests
            refresh daily — no manual generate step.
          </p>
          {lastRefresh && (
            <p className="muted tiny">Last digest refresh: {new Date(lastRefresh).toLocaleString()}</p>
          )}
        </div>
      </header>

      <form className="card form row" onSubmit={(e) => void onSearch(e)}>
        <label className="grow">
          Search ticker or name
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="AAPL or Apple"
          />
        </label>
        <button type="submit" disabled={busy}>
          Search
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {results.length > 0 && (
        <section className="card">
          <h2>Search results</h2>
          <ul className="list">
            {results.map((company) => (
              <li key={company.id}>
                <div>
                  <strong>{company.ticker}</strong> — {company.name}
                  {company.exchange ? ` (${company.exchange})` : ''}
                </div>
                <button type="button" disabled={busy} onClick={() => void onAdd(company)}>
                  Add
                </button>
              </li>
            ))}
          </ul>
        </section>
      )}

      <section>
        <h2>Your companies</h2>
        {items.length === 0 ? (
          <div className="card">
            <p className="muted">No companies yet. Search above to add your first one.</p>
          </div>
        ) : (
          <div className="ticker-grid">
            {items.map((item) => (
              <article key={item.id} className="ticker-card">
                <Link
                  className="ticker-card-link"
                  to={`/companies/${item.company.ticker}`}
                >
                  <p className="eyebrow">{item.company.exchange ?? 'Equity'}</p>
                  <h3 className="ticker-symbol">{item.company.ticker}</h3>
                  <p className="ticker-name">{item.company.name}</p>
                  <p className="ticker-meta">
                    {item.today_item_count > 0
                      ? `${item.today_item_count} update${item.today_item_count === 1 ? '' : 's'} today`
                      : 'Waiting on daily refresh'}
                  </p>
                </Link>
                <button
                  type="button"
                  className="ghost ticker-remove"
                  disabled={busy}
                  onClick={() => void onRemove(item.id)}
                >
                  Remove
                </button>
              </article>
            ))}
          </div>
        )}
      </section>
    </main>
  )
}
