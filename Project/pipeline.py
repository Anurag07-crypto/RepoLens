import sys 
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from Project.core.state import get_app_state
from Project.indexing.data_ingestion import git_ingestion

def data_load(repo_url):
    build_repository(repo_url)

def build_repository(repo_url):
    state = get_app_state()
    documents = git_ingestion(repo_url)
    state.indexer.index_repository(documents)