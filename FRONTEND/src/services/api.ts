import axios from 'axios'

const api = axios.create({
  baseURL: (import.meta.env.VITE_API_URL as string | undefined) || 'http://127.0.0.1:8000',
  timeout: 600000
})

export async function linkRepository(repoLink: string) {
  const { data } = await api.post('/link', { repo_link: repoLink })
  return data
}

export async function askRepository(query: string) {
  const { data } = await api.post('/main', { query })
  return data
}

export default api
