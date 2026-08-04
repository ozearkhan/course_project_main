from langgraph_workflow.state import TripState

from memory.memory_service import (
    load_preferences,
    load_trip_history,
)


def load_traveler_context(state: TripState):

    preferences = load_preferences(
        state["traveler_name"]
    )

    history = load_trip_history(
        state["traveler_name"]
    )

    state["traveler_preferences"] = preferences
    state["traveler_history"] = history

    return state