import { useEffect, useMemo, useRef, useState } from 'react'
import { motion } from 'framer-motion'
import { Bot, LoaderCircle, Send } from 'lucide-react'
import toast from 'react-hot-toast'
import ReactMarkdown from 'react-markdown'
import type { ComponentProps } from 'react'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import remarkGfm from 'remark-gfm'
import Layout from '@/components/Layout'
import { askRepository, linkRepository } from '@/services/api'
import type { ChatResponse, Message, RepositoryState } from '@/types'

const suggestedQuestions = ['Summarize repository', 'Explain architecture', 'Explain authentication', 'Find API endpoints', 'Show folder structure', 'Explain database']

function createMessage(role: Message['role'], content: string): Message {
  return { id: crypto.randomUUID(), role, content, createdAt: new Date().toISOString() }
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([])
  const [repoInput, setRepoInput] = useState('')
  const [chatInput, setChatInput] = useState('')
  const [repoState, setRepoState] = useState<RepositoryState>({ repoUrl: '', status: 'idle', message: 'Paste a GitHub URL to begin.' })
  const [isLoading, setIsLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement | null>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  const handleRepoLoad = async () => {
    const repoUrl = repoInput.trim()
    if (!repoUrl) {
      toast.error('Please enter a GitHub repository URL first.')
      return
    }

    setIsLoading(true)
    setRepoState({ repoUrl, status: 'loading', message: 'Indexing repository and building knowledge graph…' })
    try {
      const data = await linkRepository(repoUrl)
      setRepoState({ repoUrl, status: 'ready', message: data?.status || 'Repository loaded successfully.' })
      toast.success('Repository loaded successfully.')
      setMessages((prev) => [...prev, createMessage('assistant', `Repository ready for analysis: ${repoUrl}`)])
      setRepoInput('')
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Could not load repository.'
      setRepoState({ repoUrl, status: 'error', message })
      toast.error(message)
    } finally {
      setIsLoading(false)
    }
  }

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault()
    if (!chatInput.trim()) return

    const question = chatInput.trim()
    const userMessage = createMessage('user', question)
    setMessages((prev) => [...prev, userMessage])
    setChatInput('')
    setIsLoading(true)

    try {
      const data = (await askRepository(question)) as ChatResponse
      const responseText = typeof data.response === 'string' ? data.response : data.response?.[0]?.content || 'No answer returned.'
      setMessages((prev) => [...prev, createMessage('assistant', responseText)])
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : 'Unable to reach the backend.'
      toast.error(message)
      setMessages((prev) => [...prev, createMessage('assistant', `I couldn't answer that yet. ${message}`)])
    } finally {
      setIsLoading(false)
    }
  }

  const repoBadge = useMemo(() => {
    switch (repoState.status) {
      case 'loading':
        return 'bg-amber-500/15 text-amber-300'
      case 'ready':
        return 'bg-emerald-500/15 text-emerald-300'
      case 'error':
        return 'bg-rose-500/15 text-rose-300'
      default:
        return 'bg-slate-500/15 text-slate-300'
    }
  }, [repoState.status])

  return (
    <Layout repoStatus={repoState.message}>
      <div className="flex h-full flex-col gap-4">
        <div className="rounded-[30px] border border-white/10 bg-slate-950/70 p-4">
          <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-sm text-slate-400">Repository Loader</p>
              <p className="text-lg font-semibold text-white">Load a GitHub repository and start asking questions</p>
            </div>
            <div className={`inline-flex w-fit items-center rounded-full px-3 py-1 text-sm ${repoBadge}`}>
              {repoState.status === 'loading' ? 'Processing' : repoState.status === 'ready' ? 'Indexed' : repoState.status === 'error' ? 'Needs attention' : 'Awaiting input'}
            </div>
          </div>

          <div className="mt-4 flex flex-col gap-3 sm:flex-row">
            <input value={repoInput} onChange={(event) => setRepoInput(event.target.value)} placeholder="https://github.com/owner/repository" className="flex-1 rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white outline-none ring-0 placeholder:text-slate-500" />
            <button onClick={handleRepoLoad} disabled={isLoading} className="rounded-2xl bg-brand-600 px-4 py-3 text-sm font-medium text-white transition hover:bg-brand-700 disabled:cursor-not-allowed disabled:opacity-60">
              {isLoading ? 'Analyzing…' : 'Analyze Repository'}
            </button>
          </div>

          <div className="mt-3 h-2 overflow-hidden rounded-full bg-white/10">
            <div className={`h-full rounded-full transition-all ${repoState.status === 'ready' ? 'w-full bg-emerald-400' : repoState.status === 'loading' ? 'w-2/3 bg-amber-400' : repoState.status === 'error' ? 'w-1/3 bg-rose-400' : 'w-0 bg-white/40'}`} />
          </div>
        </div>

        <div className="flex-1 overflow-hidden rounded-[30px] border border-white/10 bg-slate-950/60 p-4">
          {messages.length === 0 ? (
            <div className="flex h-full flex-col justify-center">
              <div className="mx-auto max-w-2xl rounded-[28px] border border-white/10 bg-gradient-to-br from-white/5 to-brand-500/10 p-6 text-center">
                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-brand-500/20 text-brand-100">
                  <Bot className="h-6 w-6" />
                </div>
                <h2 className="mt-4 text-2xl font-semibold text-white">Start exploring your repository</h2>
                <p className="mt-2 text-sm leading-7 text-slate-400">Ask anything from architecture to database design. RepoLens will ground its answers with your repository context.</p>
                <div className="mt-6 flex flex-wrap justify-center gap-2">
                  {suggestedQuestions.map((question) => (
                    <button key={question} onClick={() => setChatInput(question)} className="rounded-full border border-white/10 bg-white/5 px-3 py-2 text-sm text-slate-300 transition hover:bg-white/10">
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          ) : (
            <div className="h-full space-y-3 overflow-y-auto pr-2">
              {messages.map((message) => (
                <motion.div key={message.id} initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }} className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-[90%] rounded-[24px] px-4 py-3 text-sm leading-7 shadow-lg ${message.role === 'user' ? 'bg-brand-600 text-white' : 'border border-white/10 bg-slate-900/90 text-slate-200'}`}>
                    {message.role === 'assistant' ? (
                      <div className="prose prose-invert max-w-none">
                        <ReactMarkdown
                          remarkPlugins={[remarkGfm]}
                          components={{
                            code({ inline, className, children, ...props }: ComponentProps<'code'> & { inline?: boolean }) {
                              const match = /language-(\w+)/.exec(className || '')
                              return !inline && match ? (
                                // @ts-expect-error - the package ships runtime JSX but lacks type definitions in this environment
                                <SyntaxHighlighter style={oneDark as never} language={match[1]} PreTag="div" {...props}>
                                  {String(children).replace(/\n$/, '')}
                                </SyntaxHighlighter>
                              ) : (
                                <code className={className} {...props}>{children}</code>
                              )
                            }
                          }}
                        >
                          {message.content}
                        </ReactMarkdown>
                      </div>
                    ) : (
                      <div>{message.content}</div>
                    )}
                  </div>
                </motion.div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="flex items-center gap-3 rounded-[24px] border border-white/10 bg-slate-900/90 px-4 py-3 text-sm text-slate-300">
                    <LoaderCircle className="h-4 w-4 animate-spin" />
                    Thinking with RepoLens…
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="rounded-[30px] border border-white/10 bg-slate-950/70 p-3">
          <div className="flex items-center gap-2 rounded-2xl border border-white/10 bg-white/5 px-3 py-2">
            <input value={chatInput} onChange={(event) => setChatInput(event.target.value)} placeholder="Ask about architecture, auth, API endpoints, or database design" className="flex-1 bg-transparent px-2 py-2 text-sm text-white outline-none placeholder:text-slate-500" />
            <button type="submit" className="rounded-2xl bg-brand-600 p-2.5 text-white transition hover:bg-brand-700">
              <Send className="h-4 w-4" />
            </button>
          </div>
        </form>
      </div>
    </Layout>
  )
}
