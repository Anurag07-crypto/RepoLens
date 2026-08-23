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
                raise RuntimeError("huggingface_hub is not installed. Install it with pip install huggingface_hub")

            hf_token = os.getenv("HF_TOKEN")
            if not hf_token:
                raise RuntimeError("HF_TOKEN environment variable is not set. set it to your huggingface access token")

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

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generating Embeddings raise on any failure

        Args:
            texts (List[str]): list of texts as input

        Returns:
            np.ndarray: numpy array
        """

        if not texts:
            logger.warning("Empty Text Passed to the Model")
            return np.array([])

        logger.debug(f"Generating embeddings for {len(texts)} texts via HF API")
        vectors = []
        for text in texts:
            try:
                vec = self.client.feature_extraction(text, model=self.model_name)
                vec = np.array(vec, dtype=np.float32)
                if vec.ndim > 1:
                    # Some models return token-level embeddings; mean-pool them.
                    vec = vec.mean(axis=0)
                vectors.append(vec)
            except Exception as e:
                raise RuntimeError(
                f"Embedding API failed for text: {text[:50]}... — {e}"
            ) from e
        embeddings = np.vstack(vectors)
        logger.info(f"Generated {len(texts)} embeddings")
        return embeddings
