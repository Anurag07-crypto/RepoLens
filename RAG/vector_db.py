import chromadb

from typing import List, Any
import os
import numpy as np

import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent.parent))
from logger import get_logger
logger = get_logger(__name__)

persistent_path = Path(__file__).parent.parent/ "data" / "vector_database"
class VECTOR_DB:
    def __init__(self,
                 persistant_dir:str=persistent_path,
                 collection_name:str="git_storage"):
        """Collects and Store information in Vector Database

        Args:
            persistant_dir (str, optional):  Defaults to persistent_path.
            collection_name (str, optional):  Defaults to "git_storage".
        """
        
        self.collection_name = collection_name
        self.persistant_dir = persistant_dir
        self.client = None
        self.collection = None
        self._initialize_store()
    
    def _initialize_store(self):
        try:
            os.makedirs(self.persistant_dir, exist_ok=True)
            self.client = chromadb.PersistentClient(self.persistant_dir)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description":"git text embeddings"}
            )

            logger.info(f"Vector Store Initialized {self.collection_name}")
            logger.debug(f"Existing Document in Collection {self.collection.count()}")
        
        except Exception as e:
            logger.error(f"Vector Store Not Initialized: {e}")
            raise RuntimeError("Vector Store Not Initialized") from e
        
    def add_documents(self, ids, documents, embeddings):
        if len(documents) != len(embeddings):
            logger.error("Length of documents and embeddings must match")
            raise RuntimeError("Length of documents and embeddings must match")
        metadatas, document_texts, embeddings_list = [], [], []
        for i, (document, embedding) in enumerate(zip(documents, embeddings)):
            metadata = dict(document.metadata)
            metadata["context"] = len(document.page_content)
            metadatas.append(metadata)
            document_texts.append(document.page_content)
            embeddings_list.append(embedding.tolist())

        self.collection.add(
            embeddings=embeddings_list,
            metadatas=metadatas,
            documents=document_texts,
            ids=[str(i) for i in ids]
        )
        logger.info(f"Information collected: {len(documents)} documents added to vector store")
        logger.info(f"Total documents in collection: {self.collection.count()}")