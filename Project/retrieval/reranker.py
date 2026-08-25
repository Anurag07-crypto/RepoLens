from huggingface_hub import InferenceClient
from typing import List
import sys
from pathlib import Path
import os

sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import get_logger
logger = get_logger(__name__)

class RERANKER:
    """
    Rerank results using the HF Inference API's text-classification task
    (bge-reranker-v2-m3 is a cross-encoder; no local model weights loaded,
    avoids OOM on constrained hosts like Render).
    """

    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3"):
        self.model_name = model_name
        self.client = None
        self._load_model()

    def _load_model(self):
        if InferenceClient is None:
            raise RuntimeError("huggingface_hub is not installed")

        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            raise RuntimeError("HF_TOKEN environment variable is not set")

        self.client = InferenceClient(token=hf_token)
        logger.info(f"Reranker client ready (HF Inference API): {self.model_name}")

    def rerank(
        self,
        query: str,
        documents: List[dict],
        top_k: int = 5
    ):
        """Rerank documents based on query relevance using HF's text_classification
        task (bge-reranker-v2-m3 is a cross-encoder classifier, not a
        sentence-similarity model)."""
        if not documents:
            return []

        contents = [doc["content"] for doc in documents]

        try:
            scores = []
            for content in contents:
                result = self.client.text_classification(
                    text=query,
                    text_pair=content,
                    model=self.model_name
                )
                # Log once so we can confirm the actual response shape in practice.
                logger.debug(f"Raw text_classification result: {result}")
                if isinstance(result, list):
                    scores.append(result[0]["score"])
                else:
                    scores.append(result["score"])
        except Exception as e:
            logger.error(f"Reranker call failed for '{self.model_name}': {e}")
            raise RuntimeError(
                f"Reranker model '{self.model_name}' failed during text_classification"
            ) from e

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
HF Inference API sentence_similarity()
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