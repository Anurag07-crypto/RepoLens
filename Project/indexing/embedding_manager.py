import re
from typing import List
import os
import numpy as np
import sys
from pathlib import Path

try:
    from huggingface_hub import InferenceClient
except ImportError:  # pragma: no cover - environment guard
    InferenceClient = None

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import get_logger

logger = get_logger(__name__)


class EMBEDDING_MANAGER:
    """Manages sentence embeddings using the Hugging Face Inference API
    (no local model weights loaded into memory), with a deterministic
    fallback if the API is unavailable or unauthenticated.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        fallback_dimension: int = 384,
    ):
        self.model_name = model_name
        self.client = None
        self.fallback_mode = False
        self.embedding_dimension = fallback_dimension
        self._load_model()

    def _load_model(self):
        try:
            if InferenceClient is None:
                raise RuntimeError("huggingface_hub is not installed")

            hf_token = os.getenv("HF_TOKEN")
            if not hf_token:
                raise RuntimeError("HF_TOKEN environment variable is not set")

            self.client = InferenceClient(token=hf_token)

            # Quick sanity call to confirm the endpoint + model work and to
            # learn the real embedding dimension (rather than assuming it).
            test_vec = self.client.feature_extraction(
                "connection test", model=self.model_name
            )
            test_vec = np.array(test_vec)
            if test_vec.ndim > 1:
                test_vec = test_vec.mean(axis=0)
            self.embedding_dimension = test_vec.shape[-1]

            logger.info(f"Embedding client ready (HF Inference API): {self.model_name}")
            logger.debug(f"Model Dimensions: {self.embedding_dimension}")

        except Exception as e:
            self.client = None
            self.fallback_mode = True
            logger.warning(
                f"Falling back to deterministic embeddings because the "
                f"HF Inference API could not be reached: {e}"
            )

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

        if self.fallback_mode or self.client is None:
            logger.debug("Generating fallback embeddings")
            return np.vstack([self._fallback_embedding(text) for text in texts])

        try:
            logger.debug("Generating Embeddings via HF Inference API")
            vectors = []
            for text in texts:
                vec = self.client.feature_extraction(text, model=self.model_name)
                vec = np.array(vec, dtype=np.float32)
                if vec.ndim > 1:
                    # Some models return token-level embeddings; mean-pool them.
                    vec = vec.mean(axis=0)
                vectors.append(vec)
            embeddings = np.vstack(vectors)
            logger.info("Embeddings Generated")
            return embeddings
        except Exception as e:
            logger.error(f"Embeddings Not Generated via API, using fallback: {e}")
            return np.vstack([self._fallback_embedding(text) for text in texts])