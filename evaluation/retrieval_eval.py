import json
import os

from rag_service import retrieve_documents, TOP_K

GOLDEN_QA_PATH = os.path.join("seed", "eval", "golden_qa.jsonl")
DATASET_NAME = "trippilot-golden-qa"


# ==========================================================
# Local, network-free metric computation (the CI gate)
# ==========================================================

def load_golden_qa(path=GOLDEN_QA_PATH):

    examples = []

    with open(path, encoding="utf-8") as f:
        for line in f:
            examples.append(json.loads(line))

    return examples


def retrieve_filenames(question: str, k: int = TOP_K):

    docs = retrieve_documents(question)

    return [doc.metadata.get("filename") for doc in docs[:k]]


def compute_metrics(examples=None, k: int = TOP_K):

    examples = examples if examples is not None else load_golden_qa()

    hits = 0
    reciprocal_ranks = []
    total_retrieved = 0

    for example in examples:

        expected = example["expected_source_doc"]
        retrieved = retrieve_filenames(example["question"], k=k)

        total_retrieved += len(retrieved)

        if expected in retrieved:
            hits += 1
            reciprocal_ranks.append(1.0 / (retrieved.index(expected) + 1))
        else:
            reciprocal_ranks.append(0.0)

    n = len(examples)

    return {
        "k": k,
        "n_examples": n,
        "recall_at_k": hits / n if n else 0.0,
        "precision_at_k": (hits / total_retrieved) if total_retrieved else 0.0,
        "mrr": sum(reciprocal_ranks) / n if n else 0.0,
    }


def compare_k_configs(k_values=(1, 4, 8), examples=None):
    """Re-run retrieval eval across k values - the 'change one variable, re-run'
    comparison. k is chosen over chunk size because it needs no re-ingest;
    chunk-size comparison would require rebuilding Chroma into a throwaway dir."""

    examples = examples if examples is not None else load_golden_qa()

    return [compute_metrics(examples=examples, k=k) for k in k_values]


# ==========================================================
# Optional LangSmith experiment (best-effort, never blocks the gate)
# ==========================================================

def target(inputs: dict) -> dict:
    return {"retrieved_filenames": retrieve_filenames(inputs["question"])}


def hit_at_k(outputs: dict, reference_outputs: dict) -> dict:
    expected = reference_outputs["expected_source_doc"]
    score = int(expected in outputs["retrieved_filenames"])
    return {"key": "hit_at_k", "score": score}


def reciprocal_rank(outputs: dict, reference_outputs: dict) -> dict:
    expected = reference_outputs["expected_source_doc"]
    retrieved = outputs["retrieved_filenames"]
    if expected in retrieved:
        return {"key": "reciprocal_rank", "score": 1.0 / (retrieved.index(expected) + 1)}
    return {"key": "reciprocal_rank", "score": 0.0}


def precision_recall_mrr_summary(outputs: list, reference_outputs: list) -> list:

    hits = 0
    total_retrieved = 0
    reciprocal_ranks = []

    for output, reference in zip(outputs, reference_outputs):
        expected = reference["expected_source_doc"]
        retrieved = output["retrieved_filenames"]
        total_retrieved += len(retrieved)
        if expected in retrieved:
            hits += 1
            reciprocal_ranks.append(1.0 / (retrieved.index(expected) + 1))
        else:
            reciprocal_ranks.append(0.0)

    n = len(outputs)

    return [
        {"key": "recall_at_k", "score": hits / n if n else 0.0},
        {"key": "precision_at_k", "score": (hits / total_retrieved) if total_retrieved else 0.0},
        {"key": "mrr", "score": sum(reciprocal_ranks) / n if n else 0.0},
    ]


def run_langsmith_experiment(examples=None, experiment_prefix="retrieval-eval", k: int = TOP_K):
    """Best-effort: uploads the dataset and runs a LangSmith experiment for the UI.
    Never raises - returns None if LangSmith is unreachable or unconfigured."""

    examples = examples if examples is not None else load_golden_qa()

    try:
        from langsmith import Client

        client = Client()

        if client.has_dataset(dataset_name=DATASET_NAME):
            dataset = client.read_dataset(dataset_name=DATASET_NAME)
        else:
            dataset = client.create_dataset(dataset_name=DATASET_NAME)
            client.create_examples(
                dataset_id=dataset.id,
                examples=[
                    {
                        "inputs": {"question": ex["question"]},
                        "outputs": {
                            "expected_source_doc": ex["expected_source_doc"],
                            "reference_answer": ex["reference_answer"],
                        },
                    }
                    for ex in examples
                ],
            )

        return client.evaluate(
            target,
            data=dataset.name,
            evaluators=[hit_at_k, reciprocal_rank],
            summary_evaluators=[precision_recall_mrr_summary],
            experiment_prefix=experiment_prefix,
            metadata={"k": k},
        )

    except Exception as exc:
        print(f"LangSmith experiment skipped (not reachable/configured): {exc}")
        return None


if __name__ == "__main__":
    metrics = compute_metrics()
    print(metrics)
    run_langsmith_experiment()
