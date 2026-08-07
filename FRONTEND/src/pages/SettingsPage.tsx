import { Link } from 'react-router-dom'
import { ArrowLeft, Info, RotateCcw, Settings2, SunMoon } from 'lucide-react'
import Layout from '@/components/Layout'
import { useTheme } from '@/contexts/ThemeContext'

export default function SettingsPage() {
  const { theme, toggleTheme } = useTheme()

  return (
    <Layout repoStatus="Backend ready for requests">
      <div className="space-y-4">
        <div className="rounded-[30px] border border-white/10 bg-slate-950/70 p-6">
          <div className="flex items-center gap-3">
            <div className="rounded-2xl bg-white/10 p-2.5">
              <Settings2 className="h-5 w-5 text-brand-100" />
            </div>
            <div>
              <p className="text-sm text-slate-400">Settings</p>
              <h2 className="text-2xl font-semibold text-white">Configure your RepoLens workspace</h2>
            </div>
          </div>

          <div className="mt-6 grid gap-4 md:grid-cols-2">
            <div className="rounded-3xl border border-white/10 bg-white/5 p-4">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-white">Backend URL</p>
                  <p className="mt-1 text-sm text-slate-400">Configured through VITE_API_URL</p>
                </div>
                <div className="rounded-full bg-brand-500/10 px-3 py-1 text-sm text-brand-100">Environment</div>
              </div>
            </div>

            <button onClick={toggleTheme} className="rounded-3xl border border-white/10 bg-white/5 p-4 text-left transition hover:bg-white/10">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-white">Theme</p>
                  <p className="mt-1 text-sm text-slate-400">{theme === 'dark' ? 'Dark mode enabled' : 'Light mode enabled'}</p>
                </div>
                <div className="rounded-full bg-white/10 p-2">
                  <SunMoon className="h-4 w-4 text-slate-200" />
                </div>
              </div>
            </button>
          </div>
        </div>

        <div className="rounded-[30px] border border-white/10 bg-slate-950/70 p-6">
          <div className="flex items-center gap-3">
            <div className="rounded-2xl bg-white/10 p-2.5">
              <RotateCcw className="h-5 w-5 text-brand-100" />
            </div>
            <div>
              <p className="text-sm text-slate-400">Actions</p>
              <h3 className="text-xl font-semibold text-white">Reset and manage your workspace</h3>
            </div>
          </div>

          <div className="mt-6 flex flex-wrap gap-3">
            <Link to="/chat" className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-200 transition hover:bg-white/10">
              <ArrowLeft className="h-4 w-4" /> Back to chat
            </Link>
            <button className="rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-slate-200 transition hover:bg-white/10">
              Clear chat history
            </button>
          </div>
        </div>

        <div className="rounded-[30px] border border-white/10 bg-slate-950/70 p-6">
          <div className="flex items-center gap-3">
            <div className="rounded-2xl bg-white/10 p-2.5">
              <Info className="h-5 w-5 text-brand-100" />
            </div>
            <div>
              <p className="text-sm text-slate-400">About</p>
              <h3 className="text-xl font-semibold text-white">RepoLens v2</h3>
            </div>
          </div>
          <p className="mt-4 text-sm leading-7 text-slate-400">
            RepoLens is an AI repository intelligence platform combining Hybrid RAG, GraphRAG, AST parsing, semantic search, BM25, repository graphs, and large language models to help teams understand codebases quickly and accurately.
          </p>
        </div>
      </div>
    </Layout>
  )
}
