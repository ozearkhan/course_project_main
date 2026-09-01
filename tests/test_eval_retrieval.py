import pytest

from evaluation.retrieval_eval import compute_metrics

# Calibrated against a real run (2026-08-04): recall_at_k=1.0, mrr=0.989,
# n_examples=45, k=4. Thresholds keep a margin below that for the CI gate.
# precision_at_k is not gated: with exactly one relevant doc per question and
# k=4, perfect recall caps precision at 1/k=0.25 by construction - it isn't a
# quality signal on its own here.
MIN_RECALL_AT_K = 0.85
MIN_MRR = 0.8


# Module-scoped fixture so the 45-question sweep (45 embeddings + Chroma
# searches) runs once and is shared by both tests below, instead of each
# test recomputing it from scratch (was 90 redundant embedding calls).
@pytest.fixture(scope="module")
def metrics():
    return compute_metrics()


def test_retrieval_metrics_computed(metrics):

    assert metrics["n_examples"] == 45
    assert 0.0 <= metrics["recall_at_k"] <= 1.0
    assert 0.0 <= metrics["precision_at_k"] <= 1.0
    assert 0.0 <= metrics["mrr"] <= 1.0


def test_retrieval_quality_gate(metrics):

    assert metrics["recall_at_k"] >= MIN_RECALL_AT_K, (
        f"Recall@k dropped to {metrics['recall_at_k']:.2f}, "
        f"below the {MIN_RECALL_AT_K} threshold."
    )
    assert metrics["mrr"] >= MIN_MRR, (
        f"MRR dropped to {metrics['mrr']:.2f}, below the {MIN_MRR} threshold."
    )
