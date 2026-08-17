# RepoLens v2

RepoLens v2 is an advanced AI-powered repository intelligence platform that combines a modern React TypeScript frontend with a sophisticated Python FastAPI backend. It loads GitHub repositories, performs comprehensive code analysis with AST parsing and semantic chunking, and enables intelligent querying through a RAG (Retrieval Augmented Generation) pipeline powered by Groq LLM.

## Features

- 🔗 **Repository Loading** — Load and index GitHub repositories via URL
- 🧠 **Advanced Code Analysis** — AST parsing and semantic code understanding
- 🔍 **Multi-Index Search** — Hybrid search using vector embeddings and BM25
- 📊 **Graph Analysis** — Repository dependency and code relationship mapping
- 💬 **Intelligent Chat Interface** — Natural language queries with context-aware answers
- 🎨 **Modern UI** — React TypeScript frontend with Tailwind CSS styling
- ⚡ **Fast Retrieval** — Reranking and query analysis for optimal results
- 🗂️ **Vector Storage** — Chrome vector database for semantic search

## Repo Structure

- `RepoLens/Backend/server.py` — FastAPI backend server with `/link` (repo loading) and `/main` (query) endpoints
- `RepoLens/FRONTEND/` — React TypeScript frontend with Vite build tooling
- `RepoLens/Project/` — Core processing pipeline modules
  - `code_analysis/` — AST parser, graph retriever, repository graph analysis
  - `indexing/` — Embeddings, BM25 indexing, semantic chunking, repository indexing
  - `retrieval/` — Query analyzer, retriever, reranker, LLM service
  - `storage/` — Vector database integration
- `RepoLens/data/` — Local vector database and indexed repository data
- `requirements.txt` — Python dependencies for backend and pipeline
- `RepoLens/FRONTEND/package.json` — Node.js dependencies for frontend

## Prerequisites

- Python 3.11+
- Node.js 18+ (for frontend development)
- Git
- Windows PowerShell (workspace environment is Windows)
- Groq API key (for LLM queries)
- Optional: Python virtual environment

## Setup

### 1. Activate Python virtual environment

```powershell
cd c:\Users\Lenovo\Desktop\Lens
.venv\Scripts\Activate.ps1
```

### 2. Configure environment variables

Create a `.env` file in the `RepoLens/Backend` directory:

```
GROQ_API_KEY=your_groq_api_key_here
```

The backend uses Groq's LLM for generating intelligent responses.

### 3. Install backend dependencies

```powershell
cd c:\Users\Lenovo\Desktop\Lens
pip install -r requirements.txt
```

### 4. Install frontend dependencies

```powershell
cd RepoLens\FRONTEND
npm install
```

## Running the Application

### Start backend

In one PowerShell terminal:

```powershell
cd c:\Users\Lenovo\Desktop\Lens\RepoLens\Backend
python server.py
```

The backend will start at `http://127.0.0.1:8000`.

API documentation available at `http://127.0.0.1:8000/docs`.

### Start frontend (Development)

In a second terminal:

```powershell
cd c:\Users\Lenovo\Desktop\Lens\RepoLens\FRONTEND
npm run dev
```

The frontend will start at `http://localhost:5173` (or another available port).

### Build frontend (Production)

```powershell
cd c:\Users\Lenovo\Desktop\Lens\RepoLens\FRONTEND
npm run build
```

The build output will be in the `dist/` directory.

## How to Use

1. **Enter Repository URL** — Paste a GitHub repository URL in the frontend interface
2. **Load Repository** — Click "Load Repo" to initialize indexing and analysis
3. **Wait for Processing** — The backend will:
   - Clone the repository
   - Parse code with AST analysis
   - Generate semantic embeddings
   - Build BM25 indexes
   - Create repository dependency graph
4. **Ask Questions** — Use natural language queries to explore the codebase
5. **Review Results** — View assistant answers with source code snippets and references

## API Endpoints

### `POST /link`

Load and index a repository.

**Request body:**

```json
{
  "repo_link": "https://github.com/owner/repository"
}
```

**Response:**

```json
{
  "status": "Repo Loaded Successfully",
  "repo": "https://github.com/owner/repository"
}
```

### `POST /main`

Query the indexed repository with natural language.

**Request body:**

```json
{
  "query": "What does this project do?",
  "top_k": 5
}
```

**Response:**

```json
{
  "query": "What does this project do?",
  "response": [
    {
      "answer": "...",
      "sources": [...]
    }
  ]
}
```

## Technology Stack

### Backend
- **Framework:** FastAPI
- **LLM:** Groq (langchain_groq)
- **Vector Database:** Chrome
- **Search:** BM25 + Vector Embeddings
- **Code Analysis:** AST Parser
- **Embeddings:** SentenceTransformers

### Frontend
- **Framework:** React 19 with TypeScript
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **UI Components:** Radix UI
- **HTTP Client:** Axios
- **Markdown Rendering:** React Markdown
- **Code Highlighting:** React Syntax Highlighter

## Troubleshooting

- **Frontend cannot connect to backend:** Verify the backend is running on `http://127.0.0.1:8000` and check CORS settings
- **Groq API errors:** Confirm `GROQ_API_KEY` is set correctly in the `.env` file
- **Repository loading hangs:** Try a smaller repository or increase timeout; check available disk space
- **Missing embeddings:** Ensure `sentence-transformers` is installed: `pip install sentence-transformers`
- **Vector database errors:** Delete cached vectors in `RepoLens/data/vector_database/` and retry

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## License

See [LICENSE](LICENSE) for details.
