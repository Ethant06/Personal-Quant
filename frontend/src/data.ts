// Sample data for the UI until the backend serves real briefings and market data.

export type Company = {
  ticker: string
  name: string
  sector: string
}

export type TermKey =
  | 'earnings'
  | 'guidance'
  | 'tenK'
  | 'interestRate'
  | 'fed'
  | 'dataCenter'
  | 'cloud'
  | 'marketCap'
  | 'peRatio'

export type Term = {
  label: string
  definition: string
  example: string
}

export type Source = {
  label: string
  href: string
}

export type Story = {
  id: string
  macro?: boolean
  tag: string
  name: string
  headline: string
  happened: string
  matters: string
  connects?: string
  uncertain: string
  terms: TermKey[]
  sources: Source[]
}

export type Range = '1D' | '1W' | '1M' | '1Y'

export const COMPANIES: Company[] = [
  { ticker: 'NVDA', name: 'Nvidia', sector: 'Semiconductors' },
  { ticker: 'AAPL', name: 'Apple', sector: 'Consumer tech' },
  { ticker: 'MSFT', name: 'Microsoft', sector: 'Software and cloud' },
  { ticker: 'AMZN', name: 'Amazon', sector: 'Retail and cloud' },
  { ticker: 'GOOGL', name: 'Alphabet (Google)', sector: 'Internet and ads' },
  { ticker: 'TSLA', name: 'Tesla', sector: 'Electric vehicles' },
  { ticker: 'COST', name: 'Costco', sector: 'Retail' },
  { ticker: 'DIS', name: 'Disney', sector: 'Media and parks' },
  { ticker: 'JPM', name: 'JPMorgan Chase', sector: 'Banking' },
]

export const DEFAULT_WATCHLIST = ['NVDA', 'AAPL', 'MSFT']

export const TERMS: Record<TermKey, Term> = {
  earnings: {
    label: 'Earnings',
    definition:
      "A company's profit over a period, usually three months (a quarter). Each quarter, public companies publish an earnings report showing their sales, costs and profit.",
    example:
      'If a coffee shop sells $10,000 of coffee in a quarter and spends $8,000 running the shop, its earnings are $2,000.',
  },
  guidance: {
    label: 'Guidance',
    definition:
      "A company's own forecast of how it expects the next quarter or year to go. It's an estimate, not a promise, and companies can change it.",
    example:
      "A company might say it expects next quarter's sales to be about the same as this quarter's.",
  },
  tenK: {
    label: '10-K',
    definition:
      'A yearly report that every US public company must file with the SEC. It covers the business, its risks and its audited financial results.',
    example:
      'The "Risk Factors" section of a 10-K lists what the company thinks could hurt its business.',
  },
  interestRate: {
    label: 'Interest rate',
    definition:
      'The cost of borrowing money, shown as a percentage per year. When rates go up, loans get more expensive for people and companies.',
    example: 'A 5% rate on a $1,000 loan costs about $50 in interest per year.',
  },
  fed: {
    label: 'Federal Reserve',
    definition:
      'The central bank of the US, often called "the Fed." It sets a benchmark interest rate that affects borrowing costs across the economy.',
    example:
      'When the Fed raises its rate, credit card and car loan rates usually go up too.',
  },
  dataCenter: {
    label: 'Data center',
    definition:
      'A building full of computers that run websites, apps and AI tools. Big tech companies spend heavily to build and fill them.',
    example:
      'When you ask a chatbot a question, the answer is computed in a data center.',
  },
  cloud: {
    label: 'Cloud computing',
    definition:
      'Renting computing power and storage over the internet instead of buying and running your own hardware.',
    example:
      'A startup can run its app on Microsoft Azure instead of buying its own servers.',
  },
  marketCap: {
    label: 'Market cap',
    definition:
      "Short for market capitalization: the total value of all of a company's shares added together. It's the share price times the number of shares.",
    example:
      'A company with 1 million shares priced at $50 each has a market cap of $50 million.',
  },
  peRatio: {
    label: 'P/E ratio',
    definition:
      "Price-to-earnings ratio: the share price divided by the company's earnings per share over the past year. People use it to compare how expensive a stock is relative to the profit behind it.",
    example:
      'A stock priced at $100 with $5 of earnings per share has a P/E ratio of 20.',
  },
}

export const STORIES: Story[] = [
  {
    id: 'FED',
    macro: true,
    tag: 'Big picture',
    name: 'US economy',
    headline: "The Fed's next interest-rate decision",
    happened:
      "The Federal Reserve's rate-setting committee meets to decide whether to raise, lower or hold its benchmark interest rate.",
    matters:
      'Interest rates change how much it costs companies to borrow and how investors value profits expected years from now. Tech companies like the ones on your watchlist are often sensitive to rate changes.',
    uncertain:
      "Officials don't announce their decision in advance, and markets often react as much to what they say about the future as to the decision itself.",
    terms: ['interestRate', 'fed'],
    sources: [
      { label: 'FRED: Federal funds rate', href: 'https://fred.stlouisfed.org/series/FEDFUNDS' },
      {
        label: 'Federal Reserve meeting calendar',
        href: 'https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm',
      },
    ],
  },
  {
    id: 'NVDA',
    tag: 'NVDA',
    name: 'Nvidia',
    headline: "Nvidia's earnings report is coming up",
    happened:
      'Nvidia publishes an earnings report every quarter showing how much it sold and how much profit it kept.',
    matters:
      'Most of Nvidia\'s sales now come from chips used in AI data centers, so people read this report for signs of how much big tech companies are still spending on AI.',
    connects:
      "Higher interest rates make it more expensive for Nvidia's customers to borrow money for new data centers, which could slow how fast they buy chips.",
    uncertain:
      "One quarter is a short window. The company's guidance for next quarter is its own estimate and can change.",
    terms: ['earnings', 'guidance', 'dataCenter'],
    sources: [{ label: 'Nvidia filings on SEC EDGAR', href: 'https://www.sec.gov/edgar/search/#/q=NVIDIA' }],
  },
  {
    id: 'AAPL',
    tag: 'AAPL',
    name: 'Apple',
    headline: 'Apple files its yearly report',
    happened:
      "Apple's financial year ends in late September, and soon after, it files its annual 10-K report with the SEC.",
    matters:
      "The 10-K is the most detailed look at Apple's business each year, including which products bring in the most money and what risks the company sees ahead.",
    connects:
      'Interest rates and prices across the economy affect how much money people have left over for things like new phones and laptops.',
    uncertain: "The report looks back at the past year. It doesn't tell you how the next year will go.",
    terms: ['tenK', 'earnings'],
    sources: [{ label: 'Apple filings on SEC EDGAR', href: 'https://www.sec.gov/edgar/search/#/q=Apple%20Inc' }],
  },
  {
    id: 'MSFT',
    tag: 'MSFT',
    name: 'Microsoft',
    headline: "Microsoft's cloud business is in focus",
    happened:
      'Each quarterly earnings report, Microsoft shares how fast its Azure cloud business is growing.',
    matters:
      "Cloud computing is one of Microsoft's biggest businesses, and companies renting computing power for AI tools are a large part of recent demand.",
    connects:
      'When borrowing is expensive, businesses sometimes delay new tech projects, which can slow how quickly they move work to the cloud.',
    uncertain:
      'Microsoft groups its cloud results in ways that can be hard to compare with competitors like Amazon and Google.',
    terms: ['cloud', 'earnings'],
    sources: [{ label: 'Microsoft filings on SEC EDGAR', href: 'https://www.sec.gov/edgar/search/#/q=Microsoft' }],
  },
]

// Placeholder quote values; replace with delayed market data from the backend.
export const QUOTE = { price: '$000.00', change: '+0.00%', marketCap: '$0.00T', peRatio: '00.0' }

export const RANGES: Range[] = ['1D', '1W', '1M', '1Y']

export const RANGE_NAMES: Record<Range, string> = {
  '1D': 'today',
  '1W': 'past week',
  '1M': 'past month',
  '1Y': 'past year',
}

// Placeholder chart shapes: SVG y values (0 = top) for 13 evenly spaced points.
export const CHART_SHAPES: Record<Range, number[]> = {
  '1D': [92, 88, 95, 84, 80, 86, 78, 74, 79, 70, 72, 66, 68],
  '1W': [120, 112, 116, 98, 104, 92, 96, 84, 90, 78, 82, 74, 70],
  '1M': [70, 82, 76, 94, 88, 102, 96, 86, 92, 80, 74, 84, 78],
  '1Y': [150, 142, 136, 140, 122, 116, 120, 98, 90, 96, 72, 64, 52],
}
