import uuid
from ..code_analysis.graph_retriever import GRAPH_RETRIEVER
class REPOSITORY_INDEXING:
    """
    Orchestrates the complete repository indexing pipeline.
    """
    
    def __init__(self,
                 ast_parser,
                 semantic_chunker,
                 repository_graph,
                 embedding_manager,
                 vector_db,
                 bm25_manager):
        
        self.ast_parser = ast_parser
        self.semantic_chunker = semantic_chunker
        self.repository_graph = repository_graph
        self.embedding_manager = embedding_manager
        self.vector_db = vector_db
        self.bm25_manager = bm25_manager
        
        self.repository_indices = {}
        self.graph_retriever = GRAPH_RETRIEVER(
            repository_graph=self.repository_graph,
            repository_indices=self.repository_indices
        )
        
    def index_repository(self, documents):
        """
        Index an entire repository.
        """
        for doc in documents:
            self.process_document(doc)
        

    def process_document(self, document):
        """
        Process a single source file through the complete indexing pipeline.
        """
        
        repository_index = self.build_repository_index(document)
        self.build_graph(repository_index)
        chunks = self.build_chunks(document)
        self.index_chunks(chunks)

    def build_repository_index(self, document):
        """
        Build repository index using AST.
        """
        file_path = document.metadata["source"]

        repository_index = self.ast_parser.build_repository_index(file_path)

        self.repository_indices[
            repository_index["file_name"]
        ] = repository_index
        return repository_index
        

    def build_graph(self, repository_index):
        """
        Update Repository_graph.
        """
        self.repository_graph.build(repository_index)
        
    def build_chunks(self, document):
        """
        Produce semantic chunks.
        """
        return self.semantic_chunker.chunk_documents([document])

    def index_chunks(self, chunks):

        chunk_ids = [
            str(uuid.uuid4())
            for _ in chunks
        ]

        embeddings = self.embedding_manager.generate_embeddings(
            [chunk.page_content for chunk in chunks]
        )

        self.vector_db.add_documents(
            chunk_ids,
            chunks,
            embeddings
        )

        for chunk_id, chunk in zip(chunk_ids, chunks):

            self.bm25_manager.add_documents(
                chunk_id,
                chunk.page_content,
                chunk.metadata
            )

        self.bm25_manager.index()
    
    def get_graph_retriever(self):
        return self.graph_retriever
    
    def get_repository_graph(self):
        return self.repository_graph

