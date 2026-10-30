import { useCallback, useState } from 'react'
import { DEFAULT_WATCHLIST } from './data.ts'
import type { TermKey } from './data.ts'
import BriefingScreen from './components/BriefingScreen.tsx'
import Header from './components/Header.tsx'
import type { AppScreen } from './components/Header.tsx'
import LoginScreen from './components/LoginScreen.tsx'
import TermDialog from './components/TermDialog.tsx'
import WatchlistScreen from './components/WatchlistScreen.tsx'
import './App.css'

function App() {
  const [loggedIn, setLoggedIn] = useState(false)
  const [screen, setScreen] = useState<AppScreen>('briefing')
  const [watchlist, setWatchlist] = useState<string[]>(DEFAULT_WATCHLIST)
  const [openTerm, setOpenTerm] = useState<TermKey | null>(null)
  const closeTerm = useCallback(() => setOpenTerm(null), [])

  function toggleFollow(ticker: string) {
    setWatchlist((current) =>
      current.includes(ticker) ? current.filter((t) => t !== ticker) : [...current, ticker],
    )
  }

  if (!loggedIn) {
    return <LoginScreen onLogin={() => setLoggedIn(true)} />
  }

  return (
    <>
      <Header
        screen={screen}
        onNavigate={setScreen}
        onLogout={() => {
          setLoggedIn(false)
          setScreen('briefing')
        }}
      />
      {screen === 'briefing' ? (
        <BriefingScreen
          watchlist={watchlist}
          onOpenTerm={setOpenTerm}
          onFindCompanies={() => setScreen('watchlist')}
        />
      ) : (
        <WatchlistScreen watchlist={watchlist} onToggleFollow={toggleFollow} />
      )}
      {openTerm && <TermDialog termKey={openTerm} onClose={closeTerm} />}
    </>
  )
}

export default App
