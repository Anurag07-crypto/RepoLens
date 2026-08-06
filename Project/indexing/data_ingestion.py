from langchain_community.document_loaders import GitLoader
import sys 
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger

logger = get_logger(__name__)

def git_ingestion(repo_link:str):
    """github repository data ingestions

    Args:
        repo_link (str): git repo link
    """
    try:
        import shutil
        from pathlib import Path
        
        repo_path = Path("./git_repo")
        
        if repo_path.exists():
            shutil.rmtree(repo_path)
            logger.info(f"Cleaned up existing repository directory: {repo_path}")
        
        docs = GitLoader(
            clone_url=repo_link,
            repo_path="./git_repo"
        )
        
        document = docs.load()
        logger.info("Git Clone Generated")
        return document
    except Exception as e:
        logger.error(f"Git Repo Not Existed or invalid repo link:{e}")
        raise RuntimeError("Git Repo Not Existed or invalid repo link") from e

