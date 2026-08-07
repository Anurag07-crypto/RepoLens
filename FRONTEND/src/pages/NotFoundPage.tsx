import { Link } from 'react-router-dom'
import { ArrowLeft, Compass } from 'lucide-react'

export default function NotFoundPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-[radial-gradient(circle_at_top_left,_rgba(91,124,255,0.24),_transparent_40%),linear-gradient(135deg,_#040713_0%,_#090d21_100%)] p-6 text-slate-50">
      <div className="w-full max-w-xl rounded-[32px] border border-white/10 bg-slate-950/70 p-8 text-center shadow-glow backdrop-blur-xl">
        <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-brand-500/20 text-brand-100">
          <Compass className="h-7 w-7" />
        </div>
        <p className="mt-6 text-sm uppercase tracking-[0.3em] text-slate-500">404</p>
        <h1 className="mt-3 text-3xl font-semibold text-white">This route doesn’t exist yet.</h1>
        <p className="mt-3 text-sm leading-7 text-slate-400">Return to the main workspace and continue exploring your repositories.</p>
        <Link to="/" className="mt-6 inline-flex items-center gap-2 rounded-full bg-brand-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-brand-700">
          <ArrowLeft className="h-4 w-4" /> Take me home
        </Link>
      </div>
    </div>
  )
}
