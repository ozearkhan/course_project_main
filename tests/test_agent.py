from agent_entry import run_agent


def test_agent():

    response = run_agent(
        "Find hotels in Paris"
    )

    assert response is not None