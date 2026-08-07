export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  createdAt: string
}

export interface RepositoryState {
  repoUrl: string
  status: 'idle' | 'loading' | 'ready' | 'error'
  message: string
}

export interface ChatResponse {
  query: string
  response: string | Array<{ content?: string; id?: string; rerank_score?: number }>
}
