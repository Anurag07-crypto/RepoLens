from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
import sys 
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent))
from Project.pipeline import data_load
from Project.retrieval.retriever import LLM_SERVICE, RETRIEVER
from Project.core.state import get_app_state
from logger import get_logger
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
logger = get_logger(__name__)

state = get_app_state()


class GIT_REPO(BaseModel):
    repo_link:str

class REQUEST(BaseModel):
    query:str

app = FastAPI()

allowed_origins = [origin.strip() for origin in os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "service": "RepoLens API"}

@app.post("/link")
def insert_link(link:GIT_REPO):
    """
    Insert GitHub Repo Link

    Args:
        link (GIT_REPO): Link of GitHub repo

    Raises:
        HTTPException: Runtime error in /link
        HTTPException: Unexpected error in /link

    Returns:
        str: repo_link
    """
    
    try:
        repo_link = link.repo_link
        logger.info(f"Loading repository: {repo_link}")
        data_load(repo_link)
        logger.info(f"Repository loaded successfully: {repo_link}")
        return {"status": "Repo Loaded Successfully", "repo": repo_link}
    except RuntimeError as e:
        logger.error(f"Runtime error in /link: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in /link: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong. please try again")
    
@app.post("/main")
def main(query:REQUEST):
    """
    main server for rag

    Args:
        query (REQUEST): User requested server

    Raises:
        HTTPException: Unexpected error in /main
        HTTPException: Runtime error in /main

    Returns:
        Dict: Dictionary of Query and Response
    """
    
    try:
        llm = ChatGroq(model="openai/gpt-oss-20b", api_key=groq_api_key)
        retriever = RETRIEVER(state.embedding_manager,
                            state.vector_db,
                            state.bm25_manager,
                            state.reranker,
                            state.query_analyzer,
                            state.graph_retriever
                            )
        llm_function = LLM_SERVICE(llm, retriever=retriever)
        query_text = query.query
        logger.info(f"Processing query: {query_text}")
        response = llm_function.call_llm(query_text)
        logger.info(f"Query processed successfully")
        return {
            "query": query_text,
            "response": response
        }
    except RuntimeError as e:
        logger.error(f"Runtime error in /main: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in /main: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="Something went wrong. please try again")
    
if __name__ == "__main__":
    reload_enabled = os.getenv("UVICORN_RELOAD", "false").lower() == "true"
    uvicorn.run("server:app", port=8000, host="127.0.0.1", reload=reload_enabled)