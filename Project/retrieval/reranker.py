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
    Rerank results using the HF Inference API's sentence-similarity task
    (no local model weights loaded, avoids OOM on constrained hosts like Render).
    """

    def __init__(self, model_name: str = "BAAI/bge-reranker-base"):
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
        """Rerank documents based on query relevance using HF's sentence_similarity."""
        if not documents:
            return []

        contents = [doc["content"] for doc in documents]

        try:
            scores = self.client.sentence_similarity(
                sentence=query,
                other_sentences=contents,
                model=self.model_name
            )
        except StopIteration:
            # No provider on HF's Inference API currently serves this model
            # for the sentence-similarity task.
            logger.error(
                f"No HF Inference provider serves '{self.model_name}' for "
                "sentence-similarity. Consider switching to a hosted reranker "
                "(e.g. Jina AI Reranker, Cohere Rerank) or a provider-supported model."
            )
            raise RuntimeError(
                f"Reranker model '{self.model_name}' is not available via any "
                "HF Inference provider for sentence-similarity."
            )

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