from evaluation.generation_eval import run_generation_eval, hallucinated_visa_case

# Calibrated against a real run (2026-08-06, llama3.1:8b app + qwen2.5:7b judge):
# avg_faithfulness_score=4.33, avg_visa_faithfulness_score=3.83 (n=45, visa n=12).
# Thresholds keep a small margin below those observed values.
MIN_AVG_FAITHFULNESS = 4.0
MIN_AVG_VISA_FAITHFULNESS = 3.8


def test_judge_catches_hallucinated_visa_requirement():

    grade = hallucinated_visa_case()

    assert grade["faithful"] is False
    assert grade["score"] <= 2


def test_generation_faithfulness_gate():

    summary = run_generation_eval()

    assert summary["avg_faithfulness_score"] >= MIN_AVG_FAITHFULNESS, (
        f"Average faithfulness dropped to {summary['avg_faithfulness_score']:.2f}, "
        f"below the {MIN_AVG_FAITHFULNESS} threshold."
    )
    assert summary["avg_visa_faithfulness_score"] >= MIN_AVG_VISA_FAITHFULNESS, (
        f"Visa-question faithfulness dropped to {summary['avg_visa_faithfulness_score']:.2f}, "
        f"below the {MIN_AVG_VISA_FAITHFULNESS} threshold."
    )
