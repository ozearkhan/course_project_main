import uuid
from langsmith import traceable
from langgraph_workflow.state import TripState
from langgraph_workflow.constants import (
    MAX_REVISIONS,
    APPROVED,
    REJECTED,
)
from memory.memory_service import (
    save_preferences,
    save_trip,
)

from langgraph_workflow.approval import request_approval

from mcp_client import call_tool


# ==========================================================
# Collect User Requirements
# ==========================================================

@traceable
def collect_requirements(state: TripState):

    state["revision_count"] = 0
    state["approval_status"] = None
    state["approval_feedback"] = None

    return state


# ==========================================================
# Search Flights & Hotels
# ==========================================================



@traceable
def search(state: TripState):

    flight_results = call_tool(
        "search_flights_tool",
        {
            "destination": state["destination"]
        },
    )

    hotel_results = call_tool(
        "search_hotels_tool",
        {
            "city": state["destination"]
        },
    )

    state["flights"] = flight_results.get("results", [])
    state["hotels"] = hotel_results.get("results", [])

    return state
# ==========================================================
# Assemble Itinerary
# ==========================================================





@traceable
def assemble_itinerary(state: TripState):


    if not state["flights"] or not state["hotels"]:


        state["final_message"] = "No itinerary could be assembled."

        return state


    index = min(
    state["revision_count"],
    len(state["flights"]) - 1,
    len(state["hotels"]) - 1,
    )

    flight = state["flights"][index]
    hotel = state["hotels"][index]


    state["selected_flight"] = flight
    state["selected_hotel"] = hotel

    flight_price = flight.get("price", 0)
    hotel_price = hotel.get("price_per_night", 0)

    state["total_cost"] = flight_price + hotel_price
    if not state.get("idempotency_key"):
        state["idempotency_key"] = str(uuid.uuid4())


    return state
# ==========================================================
# Budget Check
# ==========================================================

@traceable
def budget_check(state: TripState):

    if state.get("total_cost", float("inf")) <= state["budget"]:
        return state

    state["revision_count"] += 1

    state["final_message"] = (
        f"Trip exceeds budget. "
        f"Revision {state['revision_count']} of {MAX_REVISIONS}."
    )

    return state


# ==========================================================
# Present Itinerary + Human Approval
# ==========================================================

@traceable
def present_options(state: TripState):

    flight = state["selected_flight"]
    hotel = state["selected_hotel"]

    state["final_message"] = f"""
Trip Option

Flight:
{flight}

Hotel:
{hotel}

Total Cost:
${state["total_cost"]}
"""

    decision = request_approval(state)

    state["approval_status"] = decision["status"]
    state["approval_feedback"] = decision.get("feedback")

    return state


# ==========================================================
# Execute Booking (Task 3 - Next Step)
# ==========================================================

@traceable
def execute_booking(state: TripState):

    if not state.get("idempotency_key"):
        state["idempotency_key"] = str(uuid.uuid4())

    booking_payload = {
        "traveler_name": state["traveler_name"],
        "flight_id": state["selected_flight"]["flight_id"],
        "hotel_id": state["selected_hotel"]["hotel_id"],
    }

    response = call_tool(
        "create_booking_tool",
        {
            "payload": booking_payload,
            "idempotency_key": state["idempotency_key"],
        },
    )

    # Successful booking
    if "booking_id" in response:

        state["booking_id"] = response["booking_id"]

        state["final_message"] = (
            f"Booking confirmed.\n"
            f"Booking ID: {response['booking_id']}"
        )

        return state

    # Duplicate booking
    if (
    response.get("error") == "Duplicate booking"
    or response.get("detail") == "Duplicate booking already exists."
    ):
        state["revision_count"] += 1

        state["approval_status"] = "conflict"

        state["final_message"] = (
        "Booking conflict detected. "
        "Searching for another itinerary..."
        )

        return state

    raise RuntimeError(f"Booking failed: {response}")
# ==========================================================
# Confirmation (Task 3 - Next Step)
# ==========================================================



@traceable
def confirm(state: TripState):

    print("\n============================")
    print("BOOKING COMPLETE")
    print("============================")
    print(state["final_message"])

    return state
# ==========================================================
# Budget Router
# ==========================================================

def budget_router(state: TripState):

    if state["total_cost"] <= state["budget"]:
        return "within_budget"

    if state["revision_count"] >= MAX_REVISIONS:
        return "budget_failed"

    return "revise"


# ==========================================================
# Approval Router
# ==========================================================

def approval_router(state: TripState):
    print("APPROVAL STATUS =", state["approval_status"])

    if state["approval_status"] == APPROVED:
        return "approved"

    return "rejected"

def booking_router(state: TripState):

    if state["approval_status"] == "conflict":
        return "retry"

    return "confirmed"