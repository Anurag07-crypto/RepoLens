# RepoLens

RepoLens is an AI-powered repository explorer built with Streamlit frontend and FastAPI backend. It loads a GitHub repository, indexes the code with a RAG pipeline, and lets you ask natural language questions about the project.

## Features

- Load a GitHub repository by URL
- Build embeddings and BM25 search indexes
- Query repository contents with a chat-style interface
- Display assistant answers in Markdown
- Custom dark-themed Streamlit UI

## Repo Structure

- `RepoLens/Backend/server.py` — backend FastAPI server exposing `/link` and `/main`
- `RepoLens/FRONTEND/frontend_server.py` — Streamlit frontend UI
- `RepoLens/RAG/` — retrieval and generation pipeline modules
- `RepoLens/data/` — local repository and vector storage data
- `requirements.txt` — root Python dependencies for the backend and shared pipeline
- `RepoLens/FRONTEND/requirements.txt` — frontend-specific dependencies

## Prerequisites

- Python 3.11+
- Git
- Windows PowerShell (workspace environment is Windows)
- Optional: virtual environment

## Setup

### 1. Activate virtual environment

```powershell
cd c:\Users\Lenovo\Desktop\Lens
.venv\Scripts\Activate.ps1
```

### 2. Install backend dependencies

```powershell
pip install -r requirements.txt
```

### 3. Install frontend dependencies

```powershell
cd RepoLens\FRONTEND
pip install -r requirements.txt
```

### 4. Set environment variables

Create a `.env` file in the project root or set the environment directly:

```powershell
$env:GROQ_API_KEY = "your_groq_api_key_here"
```

The backend uses `GROQ_API_KEY` for the `langchain_groq.ChatGroq` model.

## Running the application

### Start backend

In one terminal:

```powershell
cd c:\Users\Lenovo\Desktop\Lens\RepoLens\Backend
python server.py
```

The backend will start at `http://127.0.0.1:8000`.

### Start frontend

In a second terminal:

```powershell
cd c:\Users\Lenovo\Desktop\Lens\RepoLens\FRONTEND
streamlit run frontend_server.py
```

Open the URL shown by Streamlit, usually `http://localhost:8501`.

## How to use

1. Paste a GitHub repository URL in the frontend.
2. Click **Load Repo** to index the repository.
3. Ask questions in the chat input.
4. Review the assistant answer and source result summaries.

## API Endpoints

### `POST /link`

Load and index a repository.

Request body:

```json
{
  "repo_link": "https://github.com/owner/repository"
}
```

Response body:

```json
{
  "status": "Repo Loaded Successfully",
  "repo": "https://github.com/owner/repository"
}
```

### `POST /main`

Ask a question to the RAG system.

Request body:

```json
{
  "query": "What does this project do?"
}
```

Response body:

```json
{
  "query": "What does this project do?",
  "response": [ ... ]
}
```

## Notes

- The backend uses `langchain`, `chromadb`, `faiss-cpu`, `sentence-transformers`, and `langchain_groq`.
- The frontend depends on `streamlit` and `requests`.
- Make sure the backend is running before submitting queries from the frontend.

## Troubleshooting

- If styles do not appear, verify `streamlit run frontend_server.py` is pointing to `RepoLens/FRONTEND/frontend_server.py`.
- If the frontend cannot connect, confirm the backend is running on `127.0.0.1:8000`.
- If the repo load hangs, try a smaller repository or restart the backend.

## License

Add your license information here.
