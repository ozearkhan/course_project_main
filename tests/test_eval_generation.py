from evaluation.generation_eval import (
    run_generation_eval,
    hallucinated_visa_case,
    calibrate_judge,
)

# Calibrated against two real runs (llama3.1:8b app + qwen2.5:7b judge):
#   2026-08-06: faithfulness=4.33, visa=3.83
#   2026-08-10: faithfulness=4.20, visa=3.83  (n=45, visa n=12)
# Faithfulness drifts with LLM variance; visa was stable. Thresholds sit well
# below the observed range so normal judge noise doesn't flake the gate, while
# a real prompt/retrieval regression (which drops these to ~1-2) still trips it.
MIN_AVG_FAITHFULNESS = 3.8
MIN_AVG_VISA_FAITHFULNESS = 3.5

# The judge must agree with the hand-labeled calibration set before we trust it.
MIN_JUDGE_AGREEMENT = 0.8


def test_judge_agrees_with_human_labels():

    result = calibrate_judge()

    assert result["agreement_rate"] >= MIN_JUDGE_AGREEMENT, (
        f"Judge agreed with only {result['agreement_rate']:.0%} of hand labels "
        f"(min {MIN_JUDGE_AGREEMENT:.0%}). Disagreements: {result['disagreements']}"
    )


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
