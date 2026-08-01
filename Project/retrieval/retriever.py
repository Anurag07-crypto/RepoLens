import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent))
from logger import get_logger
from ..indexing.embedding_manager import EMBEDDING_MANAGER
from ..storage.vector_db import VECTOR_DB
from ..indexing.bm25_manager import BM25_MANAGER
from .reranker import RERANKER
from .query_analyzer import QUERY_ANALYZER
from ..code_analysis.graph_retriever import GRAPH_RETRIEVER

logger = get_logger(__name__)

class RETRIEVER:
    """
    Retriever that helps to retrieve the docs from the storage
    """
    
    def __init__(self,
                 embedding_manager:EMBEDDING_MANAGER,
                 vector_db:VECTOR_DB,
                 bm25_manager:BM25_MANAGER,
                 reranker:RERANKER,
                 query_analyzer:QUERY_ANALYZER,
                 graph_retriever:GRAPH_RETRIEVER
                 ):
        self.embedding_manager = embedding_manager
        self.vector_db = vector_db
        self.bm25_manager = bm25_manager
        self.reranker = reranker
        self.query_analyzer = query_analyzer
        self.graph_retriever = graph_retriever
    
    def _get_top_k(self, intent:str):
        if intent=="explain":
            return 5
        elif intent=="find":
            return 3
        elif intent=="summarize":
            return 10
        elif intent=="compare":
            return 8
        return 5 
            
    def retrieve(
                self,
                query:str,
                top_k:int=4,
                threshold:float=0.3,
                filters:dict|None=None
                ):
        """
        retrieving function for retrieval

        Args:
            query (str): user query
            top_k (int, optional): Top results in k. Defaults to 4.
            threshold (float, optional): minimum passing critria. Defaults to 0.3.
        """
        
        try:
            analysed_query = self.query_analyzer.analyzer(query)
            intent = analysed_query["intent"]
            top_k = self._get_top_k(intent)
            semantic_query = analysed_query["semantic_query"]
            filters = analysed_query["filters"]
            
            dense_results = self.dense_search(
                semantic_query,
                top_k,
                threshold,
                filters= filters)
            
            dense_results = [   self.graph_retriever.enrich_document(doc)
                                for doc in dense_results
                            ]
            
            keyword_results = self.bm25_manager.keyword_search(
                semantic_query,
                top_k=top_k,
                filters=filters
            )
            
            # Hybrid Fusion starts here
            fusion_scores = {}
            document_lookup = {}
            DENSE_WEIGHT = 0.7
            BM25_WEIGHT = 0.3
            for rank, doc in enumerate(dense_results):
                score =DENSE_WEIGHT* (1/(60+rank+1)) #RRF (Reciprocal Reverse Formula)
                
                fusion_scores[doc["id"]] = score
                document_lookup[doc["id"]] = doc
            
            for rank, doc in enumerate(keyword_results):
                score = BM25_WEIGHT* (1/(60+rank+1))
                
                if doc["id"] not in document_lookup:
                    document_lookup[doc["id"]] = doc
                
                if doc["id"] in fusion_scores:
                    fusion_scores[doc["id"]] += score
        
                    
                else:
                    fusion_scores[doc["id"]] = score
                    
            
            sorted_docs = sorted(
                                fusion_scores.items(),
                                key=lambda x:x[1],
                                reverse=True
                            )
            final_documents = []
            
            for doc_id, score in sorted_docs:
                doc = document_lookup[doc_id]
                doc["rrf_score"] = score
                final_documents.append(doc)
                
            # Reranker part
            final_documents = self.reranker.rerank(
                query,
                final_documents,
                top_k=top_k
            )
            
            return final_documents
        
        except Exception as e:
            logger.error(f"Retrieval Failed: {e}")
            raise RuntimeError("Retrieval Failed") from e
            
    def dense_search(
                    self,
                    query:str,
                    top_k:int,
                    threshold:float,
                    filters = None
                    ):
        """
        Dense Search For retrieving documents from ChromaDB

        Args:
            query (str): User Query
            top_k (int): Top Results by retrieval from K
            threshold (float): Minimum score to cross the retrieval requirements
            filters (_type_, optional): MetaData Filters to filter out. Defaults to None.
        """
        
        query_embeddings = self.embedding_manager.generate_embeddings([query])[0]
        
        query_args = {
                    "query_embeddings": [query_embeddings.tolist()],
                    "include": [
                        "metadatas",
                        "distances",
                        "documents"
                    ],
                    "n_results": top_k
                    }

        if filters:
            query_args["where"] = filters

        results = self.vector_db.collection.query(**query_args)
        logger.info(f"Retrieved {len(results['ids'][0])} dense documents")

        for metadata in results["metadatas"][0]:
            logger.info(metadata)
            
        dense_docs = []
        ids = results["ids"][0]
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]
        
        for (doc_id, document, metadata, distance) in zip(
            ids,
            documents,
            metadatas,
            distances
        ):
            similarity = 1-distance
            logger.info(f'''
                        Accepted ✅ |
                        {metadata.get("file_name")}
                        Similarity = {similarity:.4f}
                        ''')
            if similarity < threshold:
                logger.info(f'''
                            Rejected ❌ |
                            {metadata.get("file_name")}
                            Similarity = {similarity:.4f}
                            ''')
                continue
            
            dense_docs.append(
                {

    "id":doc_id,

    "content":document,

    "metadata":metadata,

    "distance":distance,

    "similarity":similarity

}
            )
        logger.info(f"Dense Search Final Documents: {len(dense_docs)}")
        return dense_docs

class LLM_SERVICE:
    def __init__(self, llm, retriever: RETRIEVER):
        # retriever is built once (with its embedding model, vector db connection,
        # BM25 index, reranker, and query analyzer already loaded) and reused across
        # every call — avoids reloading everything on each question.
        self.llm = llm
        self.retriever = retriever

    @staticmethod
    def _format_context(documents: list[dict]) -> str:
        """Turn retrieved documents into clean, readable text for the prompt
        instead of dumping raw Python dict reprs."""
        if not documents:
            return "No relevant context was found."

        blocks = []
        for i, doc in enumerate(documents, 1):
            metadata = doc.get("metadata", {}) or {}
            file_name = metadata.get("file_name", "unknown_file")
            content = doc.get("content", "")
            score = doc.get("rerank_score", doc.get("rrf_score"))
            score_line = f"Relevance: {score:.4f}" if isinstance(score, (int, float)) else ""

            blocks.append(
                f"[{i}] File: {file_name}\n{score_line}\n```\n{content}\n```"
            )
        return "\n\n".join(blocks)

    def call_llm(self, user_query: str) -> str:
        try:
            rag_response = self.retriever.retrieve(user_query)
        except RuntimeError as e:
            logger.error(f"Retrieval failed for query '{user_query}': {e}")
            return "The provided repository context could not be retrieved due to an internal error."

        context = self._format_context(rag_response)

        PROMPT = f"""
Use ONLY the context to answer.

If the answer isn't in the context, say:
"The provided repository context does not contain enough information to answer this question."

Return concise Markdown.
- Mention relevant `files`, `classes`, `functions`.
- Prefer source code over docs.
- No hallucinations or filler.

Q: {user_query}

Context:
{context}
"""

        try:
            response = self.llm.invoke(PROMPT)
            return response.content
        except Exception as e:
            logger.error(f"LLM invocation failed for query '{user_query}': {e}")
            return "The assistant could not generate a response due to an internal error. Please try again."
        
        
        