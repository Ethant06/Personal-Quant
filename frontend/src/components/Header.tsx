import Logo from './Logo.tsx'

export type AppScreen = 'briefing' | 'watchlist'

type HeaderProps = {
  screen: AppScreen
  onNavigate: (screen: AppScreen) => void
  onLogout: () => void
}

function Header({ screen, onNavigate, onLogout }: HeaderProps) {
  const tabClass = (target: AppScreen) => (screen === target ? 'nav-tab nav-tab--active' : 'nav-tab')

  return (
    <header className="header">
      <div className="header-inner">
        <Logo />
        <nav aria-label="Main" className="nav">
          <button
            type="button"
            className={tabClass('briefing')}
            aria-current={screen === 'briefing' ? 'page' : undefined}
            onClick={() => onNavigate('briefing')}
          >
            Today
          </button>
          <button
            type="button"
            className={tabClass('watchlist')}
            aria-current={screen === 'watchlist' ? 'page' : undefined}
            onClick={() => onNavigate('watchlist')}
          >
            Watchlist
          </button>
        </nav>
        <div className="spacer" />
        <button type="button" className="btn btn--outline" onClick={onLogout}>
          Log out
        </button>
      </div>
    </header>
  )
}

export default Header
