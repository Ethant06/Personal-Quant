import { useState } from 'react'
import { TERMS } from '../data.ts'
import type { Story, TermKey } from '../data.ts'
import StockPanel from './StockPanel.tsx'

type StoryCardProps = {
  story: Story
  defaultExpanded?: boolean
  onOpenTerm: (term: TermKey) => void
}

function StoryCard({ story, defaultExpanded = false, onOpenTerm }: StoryCardProps) {
  const [expanded, setExpanded] = useState(defaultExpanded)
  const [tab, setTab] = useState<'story' | 'stock'>('story')
  const isCompany = !story.macro
  const showStock = isCompany && tab === 'stock'

  return (
    <article className="card">
      <div className="card-meta">
        <span className={story.macro ? 'tag tag--macro' : 'tag'}>{story.tag}</span>
        <span className="muted small">{story.name}</span>
      </div>
      <h2 className="card-title">{story.headline}</h2>

      {isCompany && (
        <div role="tablist" aria-label={`${story.name} details`} className="tabs">
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'story'}
            className={tab === 'story' ? 'tab tab--active' : 'tab'}
            onClick={() => setTab('story')}
          >
            Story
          </button>
          <button
            type="button"
            role="tab"
            aria-selected={tab === 'stock'}
            className={tab === 'stock' ? 'tab tab--active' : 'tab'}
            onClick={() => setTab('stock')}
          >
            Stock
          </button>
        </div>
      )}

      {showStock ? (
        <StockPanel onOpenTerm={onOpenTerm} />
      ) : (
        <>
          <section className="stack-xs">
            <h3 className="eyebrow">What happened</h3>
            <p className="body">{story.happened}</p>
          </section>

          {expanded && (
            <>
              <section className="stack-xs">
                <h3 className="eyebrow">Why it may matter</h3>
                <p className="body">{story.matters}</p>
              </section>
              {story.connects && (
                <section className="stack-xs">
                  <h3 className="eyebrow eyebrow--macro">How the big picture connects</h3>
                  <p className="body">{story.connects}</p>
                </section>
              )}
              <section className="uncertain stack-xs">
                <h3 className="eyebrow">What's uncertain</h3>
                <p>{story.uncertain}</p>
              </section>
              <div className="sources">
                <span className="muted">Sources:</span>
                {story.sources.map((source) => (
                  <a key={source.href} href={source.href} target="_blank" rel="noopener noreferrer">
                    {source.label}
                  </a>
                ))}
              </div>
            </>
          )}

          <div className="card-footer">
            <div className="terms">
              <span className="muted small">Terms:</span>
              {story.terms.map((key) => (
                <button key={key} type="button" className="term-chip" onClick={() => onOpenTerm(key)}>
                  {TERMS[key].label}
                </button>
              ))}
            </div>
            <button
              type="button"
              className="btn btn--ghost"
              aria-expanded={expanded}
              onClick={() => setExpanded(!expanded)}
            >
              {expanded ? 'Show less' : 'Why it may matter'}
            </button>
          </div>
        </>
      )}
    </article>
  )
}

export default StoryCard
