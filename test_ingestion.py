import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from logger import get_logger
from Project.indexing.data_ingestion import git_ingestion

logger = get_logger(__name__)

# Test repository
repo_link = 'https://github.com/Anurag07-crypto/chatbot.git'

logger.info(f"Starting git ingestion for: {repo_link}")

try:
    # Test git ingestion
    documents = git_ingestion(repo_link)
    
    logger.info(f"Successfully loaded {len(documents)} documents")
    
    for i, doc in enumerate(documents[:5]):  # Show first 5 docs
        logger.info(f"\nDocument {i}:")
        logger.info(f"  Source: {doc.metadata['source']}")
        logger.info(f"  Page content length: {len(doc.page_content)}")
        logger.info(f"  Page content preview: {doc.page_content[:200]}...")
    
    logger.info("\nAll documents loaded successfully!")
    
except Exception as e:
    logger.error(f"Error during test: {e}", exc_info=True)
    raise
