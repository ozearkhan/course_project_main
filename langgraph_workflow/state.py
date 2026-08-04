from typing import TypedDict, Optional, List, Dict


class TripState(TypedDict):
    # ======================================================
    # User Input
    # ======================================================

    traveler_name: str
    origin: str
    destination: str
    departure_date: str
    return_date: str
    budget: float

    # ======================================================
    # Semantic Memory (Module 5)
    # ======================================================

    traveler_preferences: Optional[Dict]

    # ======================================================
    # Episodic Memory (Module 5)
    # ======================================================

    traveler_history: List[Dict]

    # ======================================================
    # Search Results
    # ======================================================

    flights: List[Dict]
    hotels: List[Dict]

    # ======================================================
    # Selected Itinerary
    # ======================================================

    selected_flight: Optional[Dict]
    selected_hotel: Optional[Dict]
    total_cost: float

    # ======================================================
    # Workflow Control
    # ======================================================

    revision_count: int
    approval_status: Optional[str]
    approval_feedback: Optional[str]

    # ======================================================
    # Booking
    # ======================================================

    booking_id: Optional[str]
    idempotency_key: Optional[str]

    # ======================================================
    # Final Response
    # ======================================================

    final_message: Optional[str]