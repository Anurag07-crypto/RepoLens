from sentence_transformers import CrossEncoder
from typing import List
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import get_logger
logger = get_logger(__name__)

class RERANKER:
    """
    Rerank the results based on encoding that creates best results
    """
    
    def __init__(self, model_name:str="BAAI/bge-reranker-base"):
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        self.model = CrossEncoder(
            self.model_name
            )
        logger.info("Model Loaded.....")
    def rerank(
        self,
        query: str,
        documents: List[dict],
        top_k: int = 5
    ):
        """Rerank documents based on query relevance."""
        if not documents:
            return []
        pairs = [
                    [query, doc["content"]]
                    for doc in documents
                ]
        
        scores = self.model.predict(pairs)
        for doc, score in zip(documents, scores):
            doc["rerank_score"] = float(score)
            
        documents.sort(
                        key=lambda x: x["rerank_score"],
                        reverse=True
                        )
        logger.info("reranking processed")
        return documents[:top_k]
    
""" Whole Logic
Receive Query
        │
        ▼
Receive Documents
        │
        ▼
Build (query, document) pairs
        │
        ▼
CrossEncoder.predict()
        │
        ▼
Attach scores
        │
        ▼
Sort by score
        │
        ▼
Return Top K
"""