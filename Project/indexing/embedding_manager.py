import re
from typing import List
import numpy as np
import sys
from pathlib import Path

try:
    from sentence_transformers import SentenceTransformer
except ImportError:  # pragma: no cover - environment guard
    SentenceTransformer = None

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger

logger = get_logger(__name__)

class EMBEDDING_MANAGER:
    """Manages sentence embeddings using SentenceTransformer with a deterministic fallback."""

    def __init__(self, model_name: str = "snowflake/arctic-embed-m", fallback_dimension: int = 384):
        self.model_name = model_name
        self.model = None
        self.fallback_mode = False
        self.embedding_dimension = fallback_dimension
        self._load_model()

    def _load_model(self):
        try:
            if SentenceTransformer is None:
                raise RuntimeError("sentence-transformers is not installed")

            self.model = SentenceTransformer(model_name_or_path=self.model_name)
            self.embedding_dimension = self.model.get_embedding_dimension()
            logger.info(f"Model_Loaded: {self.model_name}")
            logger.debug(f"Model Dimensions: {self.embedding_dimension}")

        except Exception as e:
            self.model = None
            self.fallback_mode = True
            logger.warning(f"Falling back to deterministic embeddings because model loading failed: {e}")

    def _fallback_embedding(self, text: str) -> np.ndarray:
        cleaned = re.sub(r"\W+", " ", text.lower()).strip()
        tokens = cleaned.split() if cleaned else [""]
        vector = np.zeros(self.embedding_dimension, dtype=np.float32)
        for token in tokens:
            index = abs(hash(token)) % self.embedding_dimension
            vector[index] += 1.0
        if vector.sum() == 0:
            vector[0] = 1.0
        return vector / max(vector.sum(), 1.0)

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
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
            if self.fallback_mode or self.model is None:
                logger.debug("Generating fallback embeddings")
                return np.vstack([self._fallback_embedding(text) for text in texts])

            logger.debug("Generating Embeddings")
            embeddings = self.model.encode(texts)
            logger.info("Embeddings Generated")
            return embeddings
        except Exception as e:
            logger.error(f"Embeddings Not Generated: {e}")
            return np.vstack([self._fallback_embedding(text) for text in texts])