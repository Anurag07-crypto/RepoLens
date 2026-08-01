import sys 
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from Project.indexing.bm25_manager import BM25_MANAGER
from Project.indexing.embedding_manager import EMBEDDING_MANAGER
from Project.storage.vector_db import VECTOR_DB
from Project.indexing.data_ingestion import git_ingestion
from Project.indexing.semantic_chunker import SEMANTIC_CHUNKER
from Project.code_analysis.ast_parser import AST_PARSER
from Project.code_analysis.repository_graph import REPOSITORY_GRAPH
from Project.indexing.repository_index import REPOSITORY_INDEXING
from logger import get_logger


logger = get_logger(__name__)

ast_parser = AST_PARSER()

repository_graph = REPOSITORY_GRAPH()

semantic_chunker = SEMANTIC_CHUNKER()

embedding_manager = EMBEDDING_MANAGER()

vector_db = VECTOR_DB()

bm25_manager = BM25_MANAGER()

indexer = REPOSITORY_INDEXING(
    ast_parser,
    semantic_chunker,
    repository_graph,
    embedding_manager,
    vector_db,
    bm25_manager
)

def build_repository(repo_url):
    documents = git_ingestion(repo_url)
    indexer.index_repository(documents)




    