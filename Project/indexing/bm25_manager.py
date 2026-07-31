from rank_bm25 import BM25Okapi
import numpy as np
import pickle
from pathlib import Path

class BM25_MANAGER:
    """
    BM25_MANAGER - to manage kewords search for better retrival and help in hybrid search
    """
    
    def __init__(self, persist_path:str=None):
        self.documents = []
        self.tokenized_documents = []
        self.doc_ids = []
        self.metadatas = []
        self.bm25 = None
        self.persistant_path = Path(persist_path) if persist_path else Path(__file__).parent.parent / "data" / "bm25_index.pkl"
        self._load()
        
    def _load(self):
        """
        Loading the BM25 Keyword searching model [BM25kapi]
        """
        
        if self.persistant_path.exists():
            with open(self.persistant_path,"rb") as f:
                state = pickle.load(f)
            self.documents = state["documents"]
            self.tokenized_documents = state["tokenized_documents"]
            self.doc_ids = state["doc_ids"]
            self.metadatas = state.get("metadatas", [])
            self.bm25 = state["bm25"]
            
    def save(self):
        """
        Saving the Model
        """
        
        self.persistant_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.persistant_path, "wb") as f:
            pickle.dump({
                "documents": self.documents,
                "tokenized_documents": self.tokenized_documents,
                "doc_ids": self.doc_ids,
                "metadatas": self.metadatas,
                "bm25": self.bm25,
            }, f)
            
    def index(self):
        """
        Indexing the BM25 Model
        """
        
        self.bm25 = BM25Okapi(
            self.tokenized_documents
        )
        self.save()
        
    def add_documents(self, doc_id, document, metadata):
        """Adding documents in the BM25 Manager

        Args:
            doc_id (int): It's the Id of the Document to retrieve
            document (docs): Document Data
            metadata (metadata): MetaData For Filteration
        """
        
        self.documents.append(document)
        self.tokenized_documents.append(document.lower().split())
        self.doc_ids.append(doc_id)
        self.metadatas.append(metadata)
    
    def keyword_search(self, query:str, top_k:int=3, filters: dict | None = None):
        """
        It's like keyword search engine

        Args:
            query (str): query provided by user
            top_k (int, optional): Number of max Outputs. Defaults to 3.
            filters (dict | None, optional): Metadata Filters. Defaults to None.

        Returns:
            List: List of id, content, metadata and bm25_score
        """
        
        if self.bm25 is None:
            return []
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = np.argsort(scores)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            metadata = self.metadatas[idx]
            if filters:
                matched = True

                for key, value in filters.items():
                    if metadata.get(key) != value:
                        matched = False
                        break

                if not matched:
                    continue
                
            results.append({
                "id":self.doc_ids[idx],
                "content":self.documents[idx],
                "metadata": self.metadatas[idx],
                "bm25_score":scores[idx]
            })
            if len(results) >= top_k:
                break
        return results