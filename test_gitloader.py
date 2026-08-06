import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from logger import get_logger
from langchain_community.document_loaders import GitLoader

logger = get_logger(__name__)

repo_link = 'https://github.com/Anurag07-crypto/chatbot.git'

try:
    logger.info(f"Attempting to clone repository from: {repo_link}")
    
    # Try loading with different approaches
    docs = GitLoader(
        clone_url=repo_link,
        repo_path="./git_repo"
    )
    
    logger.info(f"GitLoader created: {docs}")
    
    document = docs.load()
    logger.info(f"Documents loaded: {len(document)}")
    
    for i, doc in enumerate(document):
        logger.info(f"Document {i} metadata: {doc.metadata}")
        logger.info(f"Document {i} source: {doc.metadata['source']}")
        
except Exception as e:
    logger.error(f"Error during git ingestion: {e}", exc_info=True)
    raise
