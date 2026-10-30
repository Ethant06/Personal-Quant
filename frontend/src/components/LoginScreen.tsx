import { useState } from 'react'
import type { FormEvent } from 'react'
import Logo from './Logo.tsx'

type LoginScreenProps = {
  onLogin: () => void
}

function LoginScreen({ onLogin }: LoginScreenProps) {
  const [mode, setMode] = useState<'login' | 'signup'>('login')
  const signup = mode === 'signup'

  // TODO: call the backend auth endpoints instead of logging in immediately.
  function handleSubmit(event: FormEvent) {
    event.preventDefault()
    onLogin()
  }

  return (
    <main className="login">
      <form className="login-card" onSubmit={handleSubmit}>
        <Logo size={32} />
        <div className="stack-sm">
          <h1 className="login-title">{signup ? 'Create your account' : 'Welcome back'}</h1>
          <p className="muted">
            {signup
              ? 'Follow companies you care about and get a plain-English briefing every morning.'
              : "Log in to see today's briefing for your watchlist."}
          </p>
        </div>
        <div className="field">
          <label htmlFor="email">Email</label>
          <input id="email" type="email" placeholder="you@school.edu" autoComplete="email" />
        </div>
        <div className="field">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            placeholder="At least 8 characters"
            autoComplete={signup ? 'new-password' : 'current-password'}
          />
        </div>
        <button type="submit" className="btn btn--primary btn--lg">
          {signup ? 'Create account' : 'Log in'}
        </button>
        <p className="login-switch">
          {signup ? 'Already have an account?' : 'New to Investory?'}{' '}
          <button type="button" className="link-button" onClick={() => setMode(signup ? 'login' : 'signup')}>
            {signup ? 'Log in' : 'Create an account'}
          </button>
        </p>
        <p className="login-note">
          Investory explains financial news so you can learn. It never predicts prices or tells you what to buy or
          sell.
        </p>
      </form>
    </main>
  )
}

export default LoginScreen
