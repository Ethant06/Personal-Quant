import { COMPANIES, STORIES } from '../data.ts'
import type { TermKey } from '../data.ts'
import StoryCard from './StoryCard.tsx'

type BriefingScreenProps = {
  watchlist: string[]
  onOpenTerm: (term: TermKey) => void
  onFindCompanies: () => void
}

const EXPANDED_BY_DEFAULT = new Set(['FED', 'NVDA'])

function BriefingScreen({ watchlist, onOpenTerm, onFindCompanies }: BriefingScreenProps) {
  const stories = STORIES.filter((story) => story.macro || watchlist.includes(story.id))
  const companyStoryCount = stories.filter((story) => !story.macro).length
  const quietCompanies = COMPANIES.filter(
    (company) => watchlist.includes(company.ticker) && !STORIES.some((story) => story.id === company.ticker),
  ).map((company) => company.name)
  const today = new Date().toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' })

  return (
    <main className="page">
      <div className="stack-sm">
        <p className="eyebrow">{today}</p>
        <h1 className="page-title">Your daily briefing</h1>
        <p className="muted lead">
          {companyStoryCount === 1 ? '1 update' : `${companyStoryCount} updates`} for your watchlist, plus the big
          picture.
        </p>
      </div>
      <p className="notice">
        Sample content: these stories and stock numbers only show the layout. They aren't real news or market data.
      </p>

      {stories.map((story) => (
        <StoryCard
          key={story.id}
          story={story}
          defaultExpanded={EXPANDED_BY_DEFAULT.has(story.id)}
          onOpenTerm={onOpenTerm}
        />
      ))}

      {quietCompanies.length > 0 && (
        <p className="quiet">No new stories today for {quietCompanies.join(', ')}.</p>
      )}

      {watchlist.length === 0 && (
        <div className="card empty">
          <h2 className="card-title">Your watchlist is empty</h2>
          <p className="muted">Follow a few companies and their news shows up here each morning.</p>
          <button type="button" className="btn btn--primary" onClick={onFindCompanies}>
            Find companies
          </button>
        </div>
      )}

      <p className="small muted">
        Investory explains news for learning. It doesn't predict prices or give buy, sell or hold advice.
      </p>
    </main>
  )
}

export default BriefingScreen
