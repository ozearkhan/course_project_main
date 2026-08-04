from langgraph.types import interrupt


def request_approval(state):

    decision = interrupt(
        {
            "itinerary": state["final_message"],
            "message": "Approve this itinerary?"
        }
    )

    return decision