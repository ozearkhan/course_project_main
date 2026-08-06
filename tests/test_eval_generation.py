import os

import pytest

from evaluation.generation_eval import run_generation_eval, hallucinated_visa_case

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
HAS_REAL_KEY = bool(GOOGLE_API_KEY) and not GOOGLE_API_KEY.startswith("paste-")

# Placeholder thresholds - tighten once real scores are observed on a machine
# with Ollama + a real Gemini key configured.
MIN_AVG_FAITHFULNESS = 4.0
MIN_AVG_VISA_FAITHFULNESS = 4.0

skip_reason = "GOOGLE_API_KEY not configured - generation eval needs a real Gemini key"


@pytest.mark.skipif(not HAS_REAL_KEY, reason=skip_reason)
def test_judge_catches_hallucinated_visa_requirement():

    grade = hallucinated_visa_case()

    assert grade["faithful"] is False
    assert grade["score"] <= 2


@pytest.mark.skipif(not HAS_REAL_KEY, reason=skip_reason)
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
