from evaluation.scenario_eval import run_all_scenarios


def test_all_booking_scenarios_match_expected_outcome():

    results = run_all_scenarios()

    assert len(results) == 10

    mismatches = [r for r in results if not r["match"]]

    assert not mismatches, f"Scenario outcome mismatches: {mismatches}"
