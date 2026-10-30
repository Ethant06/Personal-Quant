import { useState, type FormEvent } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'
import { supabase } from '../lib/supabase'

type Mode = 'login' | 'signup'

export function LoginPage() {
  const { session, loading } = useAuth()
  const [mode, setMode] = useState<Mode>('login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [info, setInfo] = useState<string | null>(null)

  if (!loading && session) {
    return <Navigate to="/watchlist" replace />
  }

  async function onSubmit(event: FormEvent) {
    event.preventDefault()
    setSubmitting(true)
    setError(null)
    setInfo(null)
    try {
      if (mode === 'login') {
        const { error: loginError } = await supabase.auth.signInWithPassword({
          email,
          password,
        })
        if (loginError) throw loginError
      } else {
        const { data, error: signupError } = await supabase.auth.signUp({
          email,
          password,
          options: { data: { display_name: email.split('@')[0] } },
        })
        if (signupError) throw signupError
        if (!data.session) {
          setInfo(
            'Account created. If email confirmation is on, check your inbox before logging in.',
          )
        }
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Authentication failed')
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <main className="page">
      <header className="header">
        <div>
          <p className="eyebrow">Investory</p>
          <h1>{mode === 'login' ? 'Sign in' : 'Create account'}</h1>
          <p className="muted">
            Personalized, beginner-friendly briefings for companies you follow.
          </p>
        </div>
      </header>

      <form className="card form" onSubmit={(e) => void onSubmit(e)}>
        <label>
          Email
          <input
            type="email"
            autoComplete="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </label>
        <label>
          Password
          <input
            type="password"
            autoComplete={mode === 'login' ? 'current-password' : 'new-password'}
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={6}
          />
        </label>
        {error && <p className="error">{error}</p>}
        {info && <p className="info">{info}</p>}
        <button type="submit" disabled={submitting}>
          {submitting ? 'Please wait…' : mode === 'login' ? 'Sign in' : 'Sign up'}
        </button>
      </form>

      <p className="switch">
        {mode === 'login' ? (
          <>
            New here?{' '}
            <button type="button" className="link" onClick={() => setMode('signup')}>
              Create an account
            </button>
          </>
        ) : (
          <>
            Already have an account?{' '}
            <button type="button" className="link" onClick={() => setMode('login')}>
              Sign in
            </button>
          </>
        )}
      </p>
    </main>
  )
}
