import streamlit as st
import requests
import json
import html
from typing import Dict, Any
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="RepoLens - RAG Repository Explorer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern styling
st.markdown("""
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body, [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: #e2e8f0;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    .main {
        background: #0f172a;
    }
    
    /* Header Styling */
    .header-container {
        background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
        padding: 3rem;
        border-radius: 16px;
        margin-bottom: 3rem;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.8),
                    0 0 30px rgba(124, 58, 237, 0.3);
        position: relative;
        overflow: hidden;
    }
    
    .header-container::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: sparkle 4s ease-in-out infinite;
    }
    
    .header-title {
        font-size: 3rem;
        font-weight: 900;
        color: white;
        margin: 0;
        text-shadow: 0 4px 20px rgba(0, 0, 0, 0.5);
        position: relative;
        z-index: 1;
        letter-spacing: -0.5px;
    }
    
    .header-subtitle {
        font-size: 1.125rem;
        color: rgba(255, 255, 255, 0.95);
        margin-top: 0.75rem;
        position: relative;
        z-index: 1;
        font-weight: 400;
    }
    
    /* Input Container */
    .input-container {
        background: #1e293b;
        padding: 2.5rem;
        border-radius: 16px;
        border: 1px solid #334155;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3),
                    0 0 20px rgba(30, 64, 175, 0.1);
        transition: all 0.3s ease;
    }
    
    .input-container:hover {
        border-color: #1e40af;
        box-shadow: 0 15px 25px -3px rgba(0, 0, 0, 0.4),
                    0 0 30px rgba(30, 64, 175, 0.2);
    }
    
    .input-label {
        color: #cbd5e1;
        font-weight: 600;
        margin-bottom: 0.75rem;
        display: block;
        font-size: 1rem;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.75rem 1.5rem;
        border-radius: 30px;
        font-size: 0.875rem;
        font-weight: 700;
        margin-top: 1.5rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    
    .status-badge:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.5);
    }
    
    .status-success {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .status-loading {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: #1f2937;
        font-weight: 800;
    }
    
    .status-error {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Chat Interface */
    .chat-container {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        max-height: 700px;
        overflow-y: auto;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3),
                    0 0 30px rgba(124, 58, 237, 0.1);
    }
    
    .message {
        margin-bottom: 1.5rem;
        padding: 1.25rem;
        border-radius: 12px;
        word-wrap: break-word;
        box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .message:hover {
        transform: translateX(2px);
        box-shadow: 0 4px 8px -2px rgba(0, 0, 0, 0.3);
    }
    
    .user-message {
        background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
        color: white;
        margin-left: 3rem;
        border-bottom-right-radius: 8px;
        border-top-right-radius: 20px;
        border-left: 3px solid #60a5fa;
    }
    
.assistant-message {
        background: linear-gradient(135deg, #4338ca 0%, #6366f1 100%);
        color: #e2e8f0;
        margin-right: 3rem;
        border-bottom-left-radius: 8px;
        border-top-left-radius: 20px;
        border-right: 3px solid #818cf8;
    }
    
    .message-time {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-top: 0.5rem;
    }
    
    /* Cards */
    .result-card {
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2),
                    0 0 15px rgba(99, 102, 241, 0.1);
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .result-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 4px;
        height: 100%;
        background: linear-gradient(180deg, #60a5fa 0%, #818cf8 100%);
        opacity: 0.7;
    }
    
    .result-card:hover {
        border-color: #475569;
        box-shadow: 0 8px 15px -3px rgba(0, 0, 0, 0.3),
                    0 0 25px rgba(99, 102, 241, 0.2);
        transform: translateY(-2px);
    }
    
    .result-title {
        color: #60a5fa;
        font-weight: 700;
        margin-bottom: 0.75rem;
        font-size: 1.125rem;
    }
    
    .result-content {
        color: #cbd5e1;
        line-height: 1.7;
        font-size: 0.95rem;
    }
    
    .result-score {
        margin-top: 1.5rem;
        font-size: 0.875rem;
        color: #94a3b8;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 1rem 2rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        font-size: 1rem;
        position: relative;
        overflow: hidden;
    }
    
    .stButton > button::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        transition: 0.5s;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.05);
        box-shadow: 0 15px 35px -5px rgba(0, 0, 0, 0.5),
                    0 5px 15px rgba(124, 58, 237, 0.4);
    }
    
    .stButton > button:hover::before {
        left: 100%;
    }
    
    .stButton > button:active {
        transform: translateY(-1px) scale(1.02);
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.5; }
    }
    
    @keyframes pulse-soft {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.8; }
    }
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0f172a;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #475569;
        border-radius: 4px;
        transition: background 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #64748b;
    }
    
    /* Text inputs */
    .stTextInput > div > div > input {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #1e40af !important;
        box-shadow: 0 0 20px rgba(30, 64, 175, 0.3) !important;
        background-color: #151e2e !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
        opacity: 0.8 !important;
    }

    /* Additional Enhancements */
    .stTextArea > div > div > textarea {
        background-color: #0f172a !important;
        color: #e2e8f0 !important;
        border: 1px solid #334155 !important;
        border-radius: 10px !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        resize: vertical !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: #1e40af !important;
        box-shadow: 0 0 20px rgba(30, 64, 175, 0.3) !important;
        background-color: #151e2e !important;
    }""", unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8000"

# Session state initialization
if "messages" not in st.session_state:
    st.session_state.messages = []
if "repo_loaded" not in st.session_state:
    st.session_state.repo_loaded = False
if "current_repo" not in st.session_state:
    st.session_state.current_repo = None
def load_repository(repo_link: str) -> Dict[str, Any]:
    """Load repository into RAG system"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/link",
            json={"repo_link": repo_link},
            timeout=300
        )
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to backend"}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"Backend error: {e.response.json().get('detail', str(e))}"}
    except Exception as e:
        return {"success": False, "error": f"Error: {str(e)}"}

def query_rag(query_text: str) -> Dict[str, Any]:
    """Query RAG system"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/main",
            json={"query": query_text},
            timeout=300
        )
        response.raise_for_status()
        return {"success": True, "data": response.json()}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to backend"}
    except requests.exceptions.HTTPError as e:
        return {"success": False, "error": f"Backend error: {e.response.json().get('detail', str(e))}"}
    except Exception as e:
        return {"success": False, "error": f"Error: {str(e)}"}

def format_message_time() -> str:
    """Format current time for messages"""
    return datetime.now().strftime("%H:%M:%S")

# Main layout
col1, col2 = st.columns([0.3, 0.7])

with col1:
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">🔍 RepoLens</h1>
        <p class="header-subtitle">AI-Powered Repository Explorer</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Repository Input Section
    st.subheader("📦 Load Repository")
    
    repo_url = st.text_input(
        "GitHub Repository URL",
        placeholder="https://github.com/owner/repository",
        help="Paste a GitHub repository URL to analyze",
        key="repo_input"
    )
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        load_btn = st.button("🚀 Load Repo", use_container_width=True)
    with col_btn2:
        clear_btn = st.button("🗑️ Clear", use_container_width=True)
    
    if load_btn and repo_url:
        with st.spinner("🔄 Loading repository... This may take several minutes for large repos"):
            result = load_repository(repo_url)
            if result["success"]:
                st.session_state.repo_loaded = True
                st.session_state.current_repo = repo_url
                st.success("✅ Repository loaded successfully!")
                st.markdown(f"""
                <div class="status-badge status-success">Repository: {repo_url}</div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"❌ {result['error']}")
    
    if clear_btn:
        st.session_state.repo_loaded = False
        st.session_state.current_repo = None
        st.session_state.messages = []
        st.rerun()
    
    # Repository Info
    if st.session_state.repo_loaded:
        st.markdown("---")
        st.subheader("ℹ️ Repository Info")
        info_col1, info_col2 = st.columns(2)
        with info_col1:
            st.markdown("""
            <div class="result-card">
                <div style="text-align: center;">
                    <div style="color: #10b981; font-size: 2rem; margin-bottom: 0.5rem;">✅</div>
                    <div style="color: #e2e8f0; font-weight: 600; font-size: 1.125rem;">Loaded</div>
                    <div style="color: #94a3b8; font-size: 0.875rem; margin-top: 0.25rem;">Repository Ready</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with info_col2:
            st.markdown(f"""
            <div class="result-card">
                <div style="text-align: center;">
                    <div style="color: #60a5fa; font-size: 2rem; margin-bottom: 0.5rem;">📁</div>
                    <div style="color: #e2e8f0; font-weight: 600; font-size: 1rem; word-break: break-all;">{st.session_state.current_repo[:30]}...</div>
                    <div style="color: #94a3b8; font-size: 0.875rem; margin-top: 0.25rem;">Repository URL</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="header-container">
        <h1 class="header-title">💬 Chat Assistant</h1>
        <p class="header-subtitle">Ask questions about your repository</p>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.repo_loaded:
        st.info("📌 Load a repository from the left panel to start asking questions.")
    else:
        # Chat display area
        st.markdown("### Conversation")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            if st.session_state.messages:
                for msg in st.session_state.messages:
                    role = msg.get("role", "")
                    content = msg.get("content", "")
                    time = msg.get("time", "")
                    if role == "assistant":
                        # Assistant: render as Markdown (no raw HTML)
                        st.markdown(f"**Assistant:**  \n\n{content}\n\n_{time}_", unsafe_allow_html=False)
                    else:
                        # User: escape to avoid Markdown/HTML injection
                        safe = html.escape(content)
                        safe_md = safe.replace("\n", "  \n")
                        st.markdown(f"**You:**  \n\n{safe_md}\n\n_{time}_", unsafe_allow_html=False)
            else:
                st.markdown("""
                <div class="chat-container" style="text-align: center; color: #94a3b8;">
                    <p>💬 Start by asking a question about the repository!</p>
                    <p style="font-size: 0.875rem;">Examples:</p>
                    <ul style="text-align: left; display: inline-block;">
                        <li>What does this project do?</li>
                        <li>Explain the authentication flow</li>
                        <li>Where is the database connection?</li>
                        <li>Summarize this repository</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # Query input
        st.markdown("### Ask a Question")
        query_text = st.text_area(
            "Type your question",
            placeholder="Ask anything about the repository...",
            height=100,
            key="query_input",
            label_visibility="collapsed"
        )
        
        col_query1, col_query2 = st.columns([0.8, 0.2])
        with col_query1:
            submit_query = st.button("🔍 Search", use_container_width=True)
        with col_query2:
            clear_chat = st.button("🗑️ Clear Chat", use_container_width=True)
        
        if clear_chat:
            st.session_state.messages = []
            st.rerun()
        
        if submit_query and query_text:
            # Add user message to history
            st.session_state.messages.append({
                "role": "user",
                "content": query_text,
                "time": format_message_time()
            })
            
            # Query the RAG system
            with st.spinner("🔄 Searching repository..."):
                result = query_rag(query_text)
            
            if result["success"]:
                response_data = result["data"]
                raw_response = response_data.get("response", "No response")

                if isinstance(raw_response, str):
                    # This is the LLM's actual generated answer (already Markdown) — render as-is
                    formatted_response = raw_response
                elif isinstance(raw_response, list):
                    # Raw retrieved chunks (e.g. a debug endpoint) — format for readability
                    lines = ["### Search Results\n"]
                    for i, doc in enumerate(raw_response, 1):
                        if isinstance(doc, dict):
                            content = doc.get("content", doc.get("page_content", str(doc)))
                            content = content if isinstance(content, str) else str(content)
                            score = doc.get("rerank_score", doc.get("rrf_score", 0))
                            score_str = f"{score:.3f}" if isinstance(score, (int, float)) else str(score)
                            lines.append(
                                f"**Result {i}:**\n\n{content[:500]}...\n\nScore: {score_str}\n\n---"
                            )
                        else:
                            lines.append(f"**Result {i}:** {doc}\n\n---")
                    formatted_response = "\n\n".join(lines)
                else:
                    formatted_response = json.dumps(raw_response, indent=2)
                
                # Add assistant response to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": formatted_response,
                    "time": format_message_time()
                })
                
                st.success("✅ Query completed!")
                st.rerun()
            else:
                st.error(f"❌ {result['error']}")
                # Remove the user message if query failed
                st.session_state.messages.pop()

# Footer
st.markdown("---")

st.markdown("""
<div style="text-align: center; color: #64748b; font-size: 0.875rem;">
    <p>🚀 RepoLens | AI-Powered Repository Analysis | v1.0</p>
    <p>Backend running on <code>http://127.0.0.1:8000</code></p>
</div>
""", unsafe_allow_html=True)