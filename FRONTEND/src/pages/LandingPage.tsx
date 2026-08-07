import { Link } from 'react-router-dom'
import { ArrowRight, BrainCircuit, Code2, Network, Sparkles } from 'lucide-react'
import { motion } from 'framer-motion'
import Layout from '@/components/Layout'

const highlights = [
  { icon: BrainCircuit, title: 'Hybrid RAG', description: 'Semantic search with BM25 and graph-aware retrieval.' },
  { icon: Network, title: 'Graph Intelligence', description: 'Repository structure and dependency relationships at a glance.' },
  { icon: Code2, title: 'AST Insights', description: 'Understand code flows and architecture instantly.' }
]

export default function LandingPage() {
  return (
    <Layout repoStatus="Ready to analyze">
      <div className="flex h-full flex-col justify-between gap-8">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="rounded-[32px] border border-white/10 bg-gradient-to-br from-brand-500/15 via-slate-900/80 to-cyan-400/10 p-8 sm:p-10">
          <div className="inline-flex items-center gap-2 rounded-full border border-brand-500/30 bg-brand-500/10 px-3 py-1 text-sm text-brand-100">
            <Sparkles className="h-4 w-4" />
            RepoLens v2 • AI Repository Intelligence Platform
          </div>
          <h1 className="mt-6 max-w-3xl text-4xl font-semibold tracking-tight text-white sm:text-5xl">
            Ask your codebase anything with elite repository intelligence.
          </h1>
          <p className="mt-4 max-w-2xl text-lg text-slate-400">
            Turn GitHub repositories into a searchable, explainable knowledge graph with LLM-powered analysis and rich architectural insight.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link to="/chat" className="inline-flex items-center gap-2 rounded-full bg-brand-600 px-5 py-3 font-medium text-white transition hover:bg-brand-700">
              Open workspace <ArrowRight className="h-4 w-4" />
            </Link>
            <Link to="/settings" className="rounded-full border border-white/10 bg-white/5 px-5 py-3 font-medium text-slate-200 transition hover:bg-white/10">
              Configure backend
            </Link>
          </div>
        </motion.div>

        <div className="grid gap-4 md:grid-cols-3">
          {highlights.map((item) => {
            const Icon = item.icon
            return (
              <motion.div key={item.title} initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="rounded-3xl border border-white/10 bg-white/5 p-5 backdrop-blur">
                <div className="rounded-2xl bg-white/10 p-3 text-brand-100">
                  <Icon className="h-5 w-5" />
                </div>
                <h3 className="mt-4 font-semibold text-white">{item.title}</h3>
                <p className="mt-2 text-sm leading-6 text-slate-400">{item.description}</p>
              </motion.div>
            )
          })}
        </div>
      </div>
    </Layout>
  )
}
