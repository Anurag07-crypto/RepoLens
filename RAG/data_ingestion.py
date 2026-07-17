from langchain_community.document_loaders import GitLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
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

def splitter(document, chunk_size:int=2000, chunk_overlap=200):
    """Splitter to split docs

    Args:
        document (_type_): documents
        chunk_overload (int, optional):  Defaults to 2000.
        chunk_overlap (int, optional):  Defaults to 200.
    """
    
    split_doc = RecursiveCharacterTextSplitter(
        chunk_overlap=chunk_overlap,
        chunk_size=chunk_size,
        separators=["\n\n\n","\n\n","\n",""]
    )
    
    chunk = split_doc.split_documents(document)
    
    for doc in chunk:
        file_path = doc.metadata.get("source", "")
        
        path = Path(file_path)
        doc.metadata["file_name"] = path.name
        doc.metadata["extension"] = path.suffix
        doc.metadata["directory"] = str(path.parent)
        doc.metadata["language"] = path.suffix.replace(".","")    
        
    logger.info("Docs Converted into Chunks")
    return chunk