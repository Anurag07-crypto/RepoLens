from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np 
import sys 
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger

logger = get_logger(__name__)

class EMBEDDING_MANAGER:
    """Manages sentence embeddings using SentenceTransformer"""
    
    def __init__(self, model_name:str="snowflake/arctic-embed-m"):
        self.model_name = model_name
        self.model = None
        self._load_model()
    
    def _load_model(self):
        try:
            self.model = SentenceTransformer(model_name_or_path=self.model_name)
            logger.info(f"Model_Loaded: {self.model_name}")
            logger.debug(f"""
                         Model Dimenstions:
                         {self.model.get_embedding_dimension()}
                         """)
            
        except OSError as e:
            logger.critical(f"Model File Not Found: {self.model_name}",e)
            raise RuntimeError(f"Model File Not Found: {self.model_name}") from e
        
        except Exception as e:
            logger.critical(f"Unexpected Error: {e}")
            raise RuntimeError(f"Unexpected Error") from e
    
    def generate_embeddings(self,texts:List[str])->np.ndarray:
        """Generating Embeddings

        Args:
            texts (List[str]): list of texts as input

        Returns:
            np.ndarray: numpy array
        """

        if not texts:
            logger.warning("Empty Text Passed to the Model")
            return np.array([])
        
        try:
            logger.debug("Generating Embeddings")
            embeddings = self.model.encode(texts)
            logger.info("Embeddings Generated")
            return embeddings
        except Exception as e:
            logger.error(f"Embeddings Not Generated: {e}")
            raise RuntimeError("Embeddings Not Generated") from e