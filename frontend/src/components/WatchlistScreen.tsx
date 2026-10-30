import { useState } from 'react'
import { COMPANIES, QUOTE } from '../data.ts'
import type { Company } from '../data.ts'

type WatchlistScreenProps = {
  watchlist: string[]
  onToggleFollow: (ticker: string) => void
}

type CompanyRowProps = {
  company: Company
  following: boolean
  onToggle: () => void
}

function CompanyRow({ company, following, onToggle }: CompanyRowProps) {
  return (
    <div className="company-row">
      <span className={following ? 'ticker ticker--following' : 'ticker'}>{company.ticker}</span>
      <div className="company-info">
        <span className="company-name">{company.name}</span>
        <span className="muted small">{company.sector}</span>
      </div>
      <div className="company-quote">
        <span className="company-price">{QUOTE.price}</span>
        <span className="small up">▲ {QUOTE.change} today</span>
      </div>
      {following ? (
        <button
          type="button"
          className="btn btn--outline"
          aria-label={`Stop following ${company.name}`}
          onClick={onToggle}
        >
          Remove
        </button>
      ) : (
        <button type="button" className="btn btn--primary" aria-label={`Follow ${company.name}`} onClick={onToggle}>
          Follow
        </button>
      )}
    </div>
  )
}

function WatchlistScreen({ watchlist, onToggleFollow }: WatchlistScreenProps) {
  const [query, setQuery] = useState('')
  const q = query.trim().toLowerCase()
  const matches = (company: Company) =>
    !q || company.name.toLowerCase().includes(q) || company.ticker.toLowerCase().includes(q)

  const following = COMPANIES.filter((company) => watchlist.includes(company.ticker) && matches(company))
  const suggestions = COMPANIES.filter((company) => !watchlist.includes(company.ticker) && matches(company))

  return (
    <main className="page">
      <div className="stack-sm">
        <h1 className="page-title">Watchlist</h1>
        <p className="muted lead">Follow companies to get them in your daily briefing.</p>
      </div>

      <div className="field">
        <label htmlFor="search">Search companies</label>
        <div className="search">
          <svg width="18" height="18" viewBox="0 0 24 24" aria-hidden="true">
            <circle cx="11" cy="11" r="7" fill="none" stroke="currentColor" strokeWidth="2" />
            <path d="M20 20l-4-4" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          </svg>
          <input
            id="search"
            type="search"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="Name or ticker, like Apple or AAPL"
          />
        </div>
      </div>

      <section className="stack-sm">
        <h2 className="eyebrow">Following ({watchlist.length})</h2>
        {following.map((company) => (
          <CompanyRow
            key={company.ticker}
            company={company}
            following
            onToggle={() => onToggleFollow(company.ticker)}
          />
        ))}
        {following.length === 0 && (
          <p className="muted">
            {watchlist.length === 0
              ? "You're not following any companies yet."
              : 'None of the companies you follow match that search.'}
          </p>
        )}
      </section>

      <section className="stack-sm">
        <h2 className="eyebrow">Add companies</h2>
        {suggestions.map((company) => (
          <CompanyRow
            key={company.ticker}
            company={company}
            following={false}
            onToggle={() => onToggleFollow(company.ticker)}
          />
        ))}
        {suggestions.length === 0 && <p className="muted">No other companies match that search.</p>}
      </section>
    </main>
  )
}

export default WatchlistScreen
