from evaluation.retrieval_eval import compute_metrics

# Baseline thresholds - initial values, tighten once real metrics are observed
# on a machine with huggingface.co access (blocked in the dev sandbox used to
# write this test).
MIN_RECALL_AT_K = 0.6
MIN_MRR = 0.5


def test_retrieval_metrics_computed():

    metrics = compute_metrics()

    assert metrics["n_examples"] == 45
    assert 0.0 <= metrics["recall_at_k"] <= 1.0
    assert 0.0 <= metrics["precision_at_k"] <= 1.0
    assert 0.0 <= metrics["mrr"] <= 1.0


def test_retrieval_quality_gate():

    metrics = compute_metrics()

    assert metrics["recall_at_k"] >= MIN_RECALL_AT_K, (
        f"Recall@k dropped to {metrics['recall_at_k']:.2f}, "
        f"below the {MIN_RECALL_AT_K} threshold."
    )
    assert metrics["mrr"] >= MIN_MRR, (
        f"MRR dropped to {metrics['mrr']:.2f}, below the {MIN_MRR} threshold."
    )
