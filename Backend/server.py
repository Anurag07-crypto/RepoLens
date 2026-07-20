from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel
import sys 
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent))
from RAG.main_pipeline import data_load
from RAG.retriever import LLM_SERVICE, RETRIEVER
from RAG.bm25_manager import BM25_MANAGER
from RAG.embedding_manager import EMBEDDING_MANAGER
from RAG.vector_db import VECTOR_DB
from RAG.reranker import RERANKER
from RAG.query_analyzer import QUERY_ANALYZER
from logger import get_logger
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")
logger = get_logger(__name__)
embedding_manager = EMBEDDING_MANAGER()
vector_db = VECTOR_DB()
bm25_manager = BM25_MANAGER()
reranker = RERANKER()
query_analyzer = QUERY_ANALYZER()

class GIT_REPO(BaseModel):
    repo_link:str

class REQUEST(BaseModel):
    query:str

app = FastAPI()

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
        retriever = RETRIEVER(embedding_manager,
                            vector_db,
                            bm25_manager,
                            reranker,
                            query_analyzer)
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