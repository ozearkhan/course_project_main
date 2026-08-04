from uuid import uuid4

from fastapi import APIRouter, Header, HTTPException

from fastapi import HTTPException

router = APIRouter(tags=["Bookings"])

# In-memory storage
BOOKINGS = {}
IDEMPOTENCY_KEYS = {}


@router.post("/bookings")
def create_booking(
    booking: dict,
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
):


    # Idempotency check
    if idempotency_key in IDEMPOTENCY_KEYS:

        booking_id = IDEMPOTENCY_KEYS[idempotency_key]

        return BOOKINGS[booking_id]

    # Simulate duplicate booking conflict
    for existing in BOOKINGS.values():

        if (
            existing["traveler_name"] == booking["traveler_name"]
            and existing["flight_id"] == booking["flight_id"]
            and existing["hotel_id"] == booking["hotel_id"]
        ):
            raise HTTPException(
                status_code=409,
                detail="Duplicate booking already exists."
            )

    booking_id = str(uuid4())

    result = {
        "booking_id": booking_id,
        "status": "confirmed",
        **booking,
    }

    BOOKINGS[booking_id] = result
    IDEMPOTENCY_KEYS[idempotency_key] = booking_id

    return result