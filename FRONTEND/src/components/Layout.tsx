import { Link, useLocation } from 'react-router-dom'
import { Bot, Home, LayoutGrid, Settings, Sparkles, SunMoon } from 'lucide-react'
import { useTheme } from '@/contexts/ThemeContext'
import { motion } from 'framer-motion'

interface LayoutProps {
  children: React.ReactNode
  repoStatus?: string
}

export default function Layout({ children, repoStatus = 'Ready to analyze' }: LayoutProps) {
  const location = useLocation()
  const { toggleTheme } = useTheme()

  const navItems = [
    { label: 'Home', to: '/', icon: Home },
    { label: 'Chat', to: '/chat', icon: Bot },
    { label: 'Settings', to: '/settings', icon: Settings }
  ]

  return (
    <div className="min-h-screen bg-transparent">
      <div className="mx-auto flex max-w-7xl flex-col gap-6 px-4 py-4 lg:flex-row lg:px-6">
        <aside className="w-full rounded-[28px] border border-white/10 bg-slate-950/60 p-4 shadow-glow backdrop-blur-xl lg:w-80">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="rounded-2xl bg-gradient-to-br from-brand-500 to-cyan-400 p-2.5">
                <Sparkles className="h-5 w-5 text-white" />
              </div>
              <div>
                <p className="text-lg font-semibold tracking-tight">RepoLens v2</p>
                <p className="text-sm text-slate-400">Hybrid repository intelligence</p>
              </div>
            </div>
            <button onClick={toggleTheme} className="rounded-full border border-white/10 bg-white/5 p-2 text-slate-300 transition hover:bg-white/10">
              <SunMoon className="h-4 w-4" />
            </button>
          </div>

          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="mt-6 rounded-3xl border border-brand-500/20 bg-gradient-to-br from-brand-500/10 to-cyan-400/10 p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-slate-400">Repository Status</p>
                <p className="mt-1 font-semibold text-slate-100">{repoStatus}</p>
              </div>
              <div className="rounded-full bg-emerald-500/20 px-3 py-1 text-xs font-medium text-emerald-300">Online</div>
            </div>
            <div className="mt-4 rounded-2xl border border-white/10 bg-slate-950/70 p-3 text-sm text-slate-300">
              Hybrid RAG • GraphRAG • AST • BM25
            </div>
          </motion.div>

          <nav className="mt-6 space-y-2">
            {navItems.map((item) => {
              const Icon = item.icon
              const active = location.pathname === item.to
              return (
                <Link key={item.to} to={item.to} className={`flex items-center gap-3 rounded-2xl px-3 py-3 text-sm transition ${active ? 'bg-white/10 text-white' : 'text-slate-400 hover:bg-white/5 hover:text-white'}`}>
                  <Icon className="h-4 w-4" />
                  {item.label}
                </Link>
              )
            })}
          </nav>

          <div className="mt-6 rounded-3xl border border-white/10 bg-white/5 p-4">
            <div className="flex items-center gap-2 text-sm text-slate-300">
              <LayoutGrid className="h-4 w-4" />
              AI Workspace
            </div>
            <p className="mt-2 text-sm leading-6 text-slate-400">
              Analyze repositories, inspect architecture, and ask grounded questions about your codebase.
            </p>
          </div>
        </aside>

        <main className="flex-1 rounded-[28px] border border-white/10 bg-slate-950/55 p-3 shadow-glow backdrop-blur-xl sm:p-4 lg:p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
