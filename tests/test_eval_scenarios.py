import pytest

from evaluation.scenario_eval import load_booking_scenarios, run_scenario

SCENARIOS = load_booking_scenarios()


# Parametrized per scenario (rather than one test looping all 10) so each
# scenario is independently distributable across pytest-xdist workers
# (`pytest tests/test_eval_scenarios.py -n auto`) - call_tool is already
# mocked and each scenario uses its own InMemorySaver/thread_id, so there's
# no shared state blocking parallel execution. Same assertion as before:
# every scenario's actual outcome must equal its expected outcome.
@pytest.mark.parametrize(
    "scenario",
    SCENARIOS,
    ids=[s["scenario_name"] for s in SCENARIOS],
)
def test_booking_scenario_matches_expected_outcome(scenario):

    actual_outcome = run_scenario(scenario)

    assert actual_outcome == scenario["expected_outcome"], (
        f"{scenario['scenario_name']}: expected {scenario['expected_outcome']}, "
        f"got {actual_outcome}"
    )
