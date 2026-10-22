import unittest

from Project.retrieval.reranker import RERANKER


class FakeInferenceClient:
    def __init__(self):
        self.calls = []

    def text_classification(self, text: dict[str, str], *, model: str):
        self.calls.append((text, model))
        return {"score": {"relevant": 0.9, "less relevant": 0.2}[text["text_pair"]]}


class RerankerTests(unittest.TestCase):
    def test_sends_query_document_pairs_and_sorts_by_score(self):
        reranker = RERANKER.__new__(RERANKER)
        reranker.model_name = "BAAI/bge-reranker-v2-m3"
        reranker.client = FakeInferenceClient()
        documents = [
            {"content": "less relevant"},
            {"content": "relevant"},
        ]

        result = reranker.rerank("query", documents, top_k=1)

        self.assertEqual(
            reranker.client.calls,
            [
                ({"text": "query", "text_pair": "less relevant"}, reranker.model_name),
                ({"text": "query", "text_pair": "relevant"}, reranker.model_name),
            ],
        )
        self.assertEqual(result, [{"content": "relevant", "rerank_score": 0.9}])


if __name__ == "__main__":
    unittest.main()
