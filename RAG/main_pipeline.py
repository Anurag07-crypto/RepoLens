import sys 
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from .bm25_manager import BM25_MANAGER
from .embedding_manager import EMBEDDING_MANAGER
from .vector_db import VECTOR_DB
from .data_ingestion import git_ingestion, splitter
from logger import get_logger
import uuid

logger = get_logger(__name__)
def data_load(repo_link):
    documents = git_ingestion(repo_link)
    chunks = splitter(document=documents)
    
    chunk_ids = [str(uuid.uuid4()) for _ in chunks]

    bm25_manager = BM25_MANAGER()
    embedding_manager = EMBEDDING_MANAGER()
    vector_db = VECTOR_DB()
    
    for chunk_id, chunk in zip(chunk_ids, chunks):
        bm25_manager.add_documents(
            chunk_id,
            chunk.page_content,
            chunk.metadata
            )
    bm25_manager.index()
    logger.info("bm25_manager indexed")
    embeddings = embedding_manager.generate_embeddings(
        [doc.page_content for doc in chunks]
        )
    vector_db.add_documents(chunk_ids, chunks, embeddings)
    logger.info("Documents added to vectorDB")




    