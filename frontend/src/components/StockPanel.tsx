import { useState } from 'react'
import { CHART_SHAPES, QUOTE, RANGE_NAMES, RANGES } from '../data.ts'
import type { Range, TermKey } from '../data.ts'

type StockPanelProps = {
  onOpenTerm: (term: TermKey) => void
}

function chartPath(points: number[]) {
  return points.map((y, i) => `${i === 0 ? 'M' : 'L'}${i * 50} ${y}`).join(' ')
}

function StockPanel({ onOpenTerm }: StockPanelProps) {
  const [range, setRange] = useState<Range>('1M')
  const points = CHART_SHAPES[range]
  // Lower y means a higher price, so the line ending at or above its start is "up".
  const up = points[points.length - 1] <= points[0]
  const line = chartPath(points)
  const trend = up ? 'up' : 'down'

  return (
    <>
      <div className="stats">
        <div className="stat">
          <span className="stat-label">Price</span>
          <span className="stat-value">{QUOTE.price}</span>
        </div>
        <div className="stat">
          <span className="stat-label">Today</span>
          <span className="stat-value up">▲ {QUOTE.change}</span>
        </div>
        <button type="button" className="stat stat--term" onClick={() => onOpenTerm('marketCap')}>
          <span className="stat-label">Market cap</span>
          <span className="stat-value">{QUOTE.marketCap}</span>
        </button>
        <button type="button" className="stat stat--term" onClick={() => onOpenTerm('peRatio')}>
          <span className="stat-label">P/E ratio</span>
          <span className="stat-value">{QUOTE.peRatio}</span>
        </button>
      </div>

      <div className="chart-box">
        <div className="chart-header">
          <div className="stack-xs">
            <h3 className="eyebrow">Price chart</h3>
            <span className={`range-change ${trend}`}>
              {up ? '▲ +0.00%' : '▼ −0.00%'} {RANGE_NAMES[range]}
            </span>
          </div>
          <div className="ranges">
            {RANGES.map((r) => (
              <button
                key={r}
                type="button"
                className={r === range ? 'range-btn range-btn--active' : 'range-btn'}
                aria-pressed={r === range}
                onClick={() => setRange(r)}
              >
                {r}
              </button>
            ))}
          </div>
        </div>
        <svg
          className={`chart chart--${trend}`}
          viewBox="0 0 600 180"
          preserveAspectRatio="none"
          role="img"
          aria-label="Placeholder price chart"
        >
          <path className="chart-grid" d="M0 45H600M0 90H600M0 135H600" vectorEffect="non-scaling-stroke" />
          <path className="chart-area" d={`${line} L600 180 L0 180 Z`} />
          <path className="chart-line" d={line} vectorEffect="non-scaling-stroke" />
        </svg>
        <p className="small muted">Placeholder chart shape. The real app would draw delayed market prices here.</p>
      </div>
    </>
  )
}

export default StockPanel
