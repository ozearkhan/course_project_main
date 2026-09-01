from evaluation.generation_eval import run_demo_generation_eval, hallucinated_visa_case

# Fast, always-run demo path (fixed 5-question file, no env vars needed) -
# NOT the quality gate. The real gate is test_eval_generation.py's
# test_generation_faithfulness_gate, which always uses the full 45.


def test_demo_generation_eval_runs():

    summary = run_demo_generation_eval()

    assert summary["n_examples"] == 5


def test_demo_catches_hallucinated_visa_requirement():

    grade = hallucinated_visa_case()

    assert grade["faithful"] is False
    assert grade["score"] <= 2
