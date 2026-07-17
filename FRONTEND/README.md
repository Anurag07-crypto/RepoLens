# RepoLens Frontend - Streamlit Application

## Overview
Modern Streamlit-based frontend for RepoLens, featuring:
- 🔍 **Git Repository Input** - Load any GitHub repository URL
- 💬 **RAG Chat Interface** - Ask questions about your repository
- 📊 **Search Results** - View ranked and reranked documents
- 🎨 **Dark Mode UI** - Modern, developer-friendly interface

## Setup Instructions

### Prerequisites
- Python 3.8+
- Backend server running on `http://127.0.0.1:8000`

### Installation

1. **Navigate to frontend directory:**
   ```bash
   cd RepoLens/FRONTEND
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

**Option 1: Run directly**
```bash
streamlit run frontend_server.py
```

**Option 2: With custom port**
```bash
streamlit run frontend_server.py --server.port 8501
```

The application will open at `http://localhost:8501`

## Features

### 1. Repository Loading
- Paste any GitHub repository URL
- Backend indexes the repository using RAG pipeline
- Status indicator shows when repository is ready
- Clear button to unload repository and reset chat

### 2. RAG Chat Interface
- **Chat History** - All conversations are preserved in session
- **Query Processing** - Ask questions about the loaded repository
- **Ranked Results** - Results show rerank scores and content
- **Error Handling** - Graceful error messages with backend feedback

### 3. UI/UX
- **Dark Theme** - Easy on the eyes with modern gradient backgrounds
- **Responsive Layout** - Two-column design (input + chat)
- **Real-time Feedback** - Loading spinners, success/error messages
- **Timestamps** - Each message shows when it was sent/received

## File Structure

```
FRONTEND/
├── frontend_server.py      # Main Streamlit application
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## API Integration

The frontend connects to these backend endpoints:

### POST /link
**Purpose:** Load and index a Git repository

**Request:**
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

### POST /main
**Purpose:** Query the RAG system about the loaded repository

**Request:**
```json
{
  "query": "What does this project do?"
}
```

**Response:**
```json
{
  "query": "What does this project do?",
  "response": [
    {
      "id": "document_id",
      "content": "Document content...",
      "rerank_score": 0.95
    }
  ]
}
```

## Configuration

**API Base URL:**
- Location: `frontend_server.py` line ~137
- Current: `http://127.0.0.1:8000`
- Change if backend runs on different host/port

**Timeout Settings:**
- Repository loading: 300 seconds
- Query search: 30 seconds

## Example Usage

1. **Start backend:**
   ```bash
   python RepoLens/Backend/server.py
   ```

2. **Start frontend (in another terminal):**
   ```bash
   streamlit run FRONTEND/frontend_server.py
   ```

3. **Load a repository:**
   - Paste: `https://github.com/langchain-ai/langchain`
   - Click "🚀 Load Repo"
   - Wait for indexing to complete

4. **Ask questions:**
   - "What is this library used for?"
   - "Show me the main components"
   - "How does authentication work?"

## Troubleshooting

### "Cannot connect to backend"
- Ensure backend is running: `python RepoLens/Backend/server.py`
- Check backend is on `http://127.0.0.1:8000`
- Verify no firewall is blocking port 8000

### "Request timeout"
- Repository is too large or being processed
- Try smaller repositories first
- Increase timeout in `frontend_server.py` if needed

### Empty chat history
- Use "🗑️ Clear Chat" to start fresh
- Chat is session-based and clears on app reload

## Future Enhancements

- [ ] File browser to view repository structure
- [ ] Streaming responses for real-time updates
- [ ] Export chat history
- [ ] Multiple repository support
- [ ] Custom RAG parameters (top_k, threshold)
- [ ] Response caching
- [ ] User authentication
- [ ] Repository metadata display

## License

Same as RepoLens main project
