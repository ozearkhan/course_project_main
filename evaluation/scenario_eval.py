import json
import os
from unittest.mock import patch

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from langgraph_workflow.graph import builder

BOOKING_SCENARIOS_PATH = os.path.join("seed", "eval", "booking_scenarios.jsonl")


def load_booking_scenarios(path=BOOKING_SCENARIOS_PATH):

    scenarios = []

    with open(path, encoding="utf-8") as f:
        for line in f:
            scenarios.append(json.loads(line))

    return scenarios


def make_call_tool_mock(scenario):

    booking_calls = {"count": 0}

    def _call_tool(tool_name, arguments):

        if tool_name == "search_flights_tool":
            return {"results": scenario["flights"]}

        if tool_name == "search_hotels_tool":
            return {"results": scenario["hotels"]}

        if tool_name == "create_booking_tool":
            booking_calls["count"] += 1
            if scenario["booking_conflict_first"] and booking_calls["count"] == 1:
                return {"detail": "Duplicate booking already exists."}
            return {"booking_id": f"TEST-{scenario['scenario_name']}"}

        raise ValueError(f"Unexpected tool_name in scenario mock: {tool_name}")

    return _call_tool


def determine_outcome(result: dict) -> str:

    if "booking_id" in result:
        return "booked"

    if result.get("approval_status") == "rejected":
        return "rejected"

    return "escalated"


def run_scenario(scenario) -> str:

    graph = builder.compile(checkpointer=InMemorySaver())

    config = {
        "configurable": {
            "thread_id": scenario["scenario_name"],
        },
    }

    state = {
        "traveler_name": scenario["traveler_name"],
        "destination": scenario["destination"],
        "budget": scenario["budget"],
    }

    with patch(
        "langgraph_workflow.nodes.call_tool",
        side_effect=make_call_tool_mock(scenario),
    ):
        result = graph.invoke(state, config=config)

        while "__interrupt__" in result:

            if scenario["human_decision"] is None:
                break

            decision = {"status": scenario["human_decision"]}
            result = graph.invoke(Command(resume=decision), config=config)

    return determine_outcome(result)


def run_all_scenarios(scenarios=None):

    scenarios = scenarios if scenarios is not None else load_booking_scenarios()

    results = []

    for scenario in scenarios:

        actual_outcome = run_scenario(scenario)

        results.append({
            "scenario_name": scenario["scenario_name"],
            "expected_outcome": scenario["expected_outcome"],
            "actual_outcome": actual_outcome,
            "match": actual_outcome == scenario["expected_outcome"],
        })

    return results


if __name__ == "__main__":
    for r in run_all_scenarios():
        print(r)
