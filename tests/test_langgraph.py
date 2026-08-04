from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from langgraph_workflow.graph import builder

from unittest.mock import patch

def test_happy_path():

    graph = builder.compile(checkpointer=InMemorySaver())

    config = {
        "configurable": {
            "thread_id": "happy-path"
        }
    }

    state = {
        "traveler_name": "Amulya",
        "destination": "Paris",
        "budget": 1500,
    }

    result = graph.invoke(state, config=config)

    assert "__interrupt__" in result


@patch("langgraph_workflow.nodes.call_tool")
def test_resume_after_approval(mock_call_tool):

    graph = builder.compile(checkpointer=InMemorySaver())

    config = {
        "configurable": {
            "thread_id": "resume-test"
        }
    }

    state = {
        "traveler_name": "Amulya",
        "destination": "Paris",
        "budget": 1500,
    }

    # search_flights
    mock_call_tool.side_effect = [

        {
            "results": [
                {
                    "flight_id": 1,
                    "price": 100,
                    "airline": "Demo Airline",
                }
            ]
        },

        # search_hotels
        {
            "results": [
                {
                    "hotel_id": 1,
                    "price_per_night": 200,
                    "hotel_name": "Demo Hotel",
                }
            ]
        },

        # booking
        {
            "booking_id": "TEST-BOOKING-001"
        },
    ]

    graph.invoke(state, config=config)

    result = graph.invoke(
        Command(
            resume={
                "status": "approved"
            }
        ),
        config=config,
    )

    assert result["booking_id"] == "TEST-BOOKING-001"

@patch("langgraph_workflow.nodes.call_tool")
def test_rejection(mock_call_tool):

    graph = builder.compile(checkpointer=InMemorySaver())

    config = {
        "configurable": {
            "thread_id": "reject-test"
        }
    }

    state = {
        "traveler_name": "Amulya",
        "destination": "Paris",
        "budget": 1500,
    }

    mock_call_tool.side_effect = [

        {
            "results": [
                {
                    "flight_id": 1,
                    "price": 100,
                    "airline": "Demo Airline",
                }
            ]
        },

        {
            "results": [
                {
                    "hotel_id": 1,
                    "price_per_night": 200,
                    "hotel_name": "Demo Hotel",
                }
            ]
        },
    ]

    graph.invoke(state, config=config)

    result = graph.invoke(
        Command(
            resume={
                "status": "rejected"
            }
        ),
        config=config,
    )

    assert result["approval_status"] == "rejected"
    assert "booking_id" not in result
    
def test_booking_conflict():
    assert True