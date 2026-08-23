from Project.retrieval.retriever import LLM_SERVICE, RETRIEVER
from Project.indexing.bm25_manager import BM25_MANAGER
from Project.indexing.embedding_manager import EMBEDDING_MANAGER
from Project.storage.vector_db import VECTOR_DB
from Project.retrieval.reranker import RERANKER
from Project.retrieval.query_analyzer import QUERY_ANALYZER
from Project.code_analysis.graph_retriever import GRAPH_RETRIEVER
from Project.indexing.repository_index import REPOSITORY_INDEXING
from Project.code_analysis.ast_parser import AST_PARSER
from Project.code_analysis.repository_graph import REPOSITORY_GRAPH
from Project.indexing.semantic_chunker import SEMANTIC_CHUNKER

_app_state= None
class _APPSTATE:
    def __init__(self):
        self.embedding_manager = EMBEDDING_MANAGER()
        self.vector_db = VECTOR_DB()
        self.bm25_manager = BM25_MANAGER()
        self.reranker = RERANKER()
        self.query_analyzer = QUERY_ANALYZER()
        self.ast_parser = AST_PARSER()
        self.semantic_chunker = SEMANTIC_CHUNKER()
        self.repository_graph = REPOSITORY_GRAPH()
        self.indexer = REPOSITORY_INDEXING(self.ast_parser,
                                    self.semantic_chunker,
                                    self.repository_graph,
                                    self.embedding_manager,
                                    self.vector_db,
                                    self.bm25_manager)
        self.graph_retriever = GRAPH_RETRIEVER(
            self.indexer.repository_graph,
            self.indexer.repository_indices
        )
        
def get_app_state():
    global _app_state
    if _app_state is None:
        _app_state = _APPSTATE()
    return _app_state