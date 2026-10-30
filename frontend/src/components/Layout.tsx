import { NavLink, Outlet } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

export function Layout() {
  const { session, signOut } = useAuth()

  return (
    <div className="shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Investory</p>
          <p className="topbar-user">{session?.user.email}</p>
        </div>
        <nav className="nav">
          <NavLink to="/watchlist">Watchlist</NavLink>
          <NavLink to="/briefing">All updates</NavLink>
          <button type="button" className="ghost" onClick={() => void signOut()}>
            Sign out
          </button>
        </nav>
      </header>
      <Outlet />
    </div>
  )
}
