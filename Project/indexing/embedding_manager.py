import hashlib
import os
import re
import sys
from pathlib import Path
from typing import List

import numpy as np

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
        fallback_dimension: int = 384,  # FIXED: matches all-MiniLM-L6-v2
    ):
        self.model_name = model_name
        self.client = None
        self.fallback_mode = False
        self.embedding_dimension = fallback_dimension
        self._load_model()

    def _load_model(self):
        try:
            if InferenceClient is None:
                raise RuntimeError(
                    "huggingface_hub is not installed. "
                    "Install it with: pip install huggingface_hub"
                )

            hf_token = os.getenv("HF_TOKEN")
            if not hf_token:
                raise RuntimeError(
                    "HF_TOKEN environment variable is not set. "
                    "Set it to your Hugging Face access token."
                )

            self.client = InferenceClient(token=hf_token)

            # Quick sanity call to learn the real embedding dimension
            test_vec = self.client.feature_extraction(
                "connection test", model=self.model_name
            )
            test_vec = np.array(test_vec)
            if test_vec.ndim > 1:
                test_vec = test_vec.mean(axis=0)
            self.embedding_dimension = int(test_vec.shape[-1])

            logger.info(
                f"Embedding client ready (HF Inference API): {self.model_name}"
            )
            logger.debug(f"Model dimensions: {self.embedding_dimension}")

        except Exception as e:
            self.client = None
            self.fallback_mode = True
            logger.warning(
                f"HF Inference API unreachable — using deterministic fallback: {e}"
            )

    def _fallback_embedding(self, text: str) -> np.ndarray:
        """Deterministic embedding using SHA256 hashing (no API needed)."""
        # Deterministic seed from text
        seed = int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:8], 16)
        rng = np.random.RandomState(seed)
        vec = rng.randn(self.embedding_dimension).astype(np.float32)
        # Normalize to unit length
        norm = np.linalg.norm(vec)
        return vec if norm == 0 else vec / norm

    def generate_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings. Never returns empty for non-empty input."""

        if not texts:
            logger.warning("Empty text passed to the model")
            return np.array([])

        logger.debug(f"Generating embeddings for {len(texts)} texts")

        vectors = []
        for text in texts:
            if self.fallback_mode or self.client is None:
                vec = self._fallback_embedding(text)
            else:
                try:
                    vec = self.client.feature_extraction(
                        text, model=self.model_name
                    )
                    vec = np.array(vec, dtype=np.float32)
                    if vec.ndim > 1:
                        vec = vec.mean(axis=0)
                except Exception as e:
                    logger.error(
                        f"HF API failed for '{text[:50]}...': {e}. "
                        f"Switching to fallback for this batch."
                    )
                    vec = self._fallback_embedding(text)

            vectors.append(vec)

        embeddings = np.vstack(vectors)
        logger.info(f"Generated {len(texts)} embeddings (dim={embeddings.shape[-1]})")
        return embeddings