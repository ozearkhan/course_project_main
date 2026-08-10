import uuid

import pytest
import requests

from langgraph_workflow.booking_service import create_booking, BASE_URL

# Bonus real-stack smoke test (not mocked): proves the actual POST /bookings
# endpoint returns a genuine 409 on a duplicate itinerary and honors the
# Idempotency-Key header. Complements the fast mocked scenario eval, which
# proves the graph's decision logic. Skips cleanly if the mock API isn't up.


def _api_running():
    try:
        requests.get(f"{BASE_URL}/docs", timeout=2)
        return True
    except requests.RequestException:
        return False


pytestmark = pytest.mark.skipif(
    not _api_running(),
    reason="mock_travel_api not running on :8000 - start it with `uvicorn mock_travel_api.main:app`",
)


def test_real_duplicate_booking_returns_409():

    traveler = f"SmokeTest-{uuid.uuid4()}"
    payload = {"traveler_name": traveler, "flight_id": 1, "hotel_id": 1}

    first = create_booking(payload, str(uuid.uuid4()))
    assert first.status_code == 200
    assert first.json()["status"] == "confirmed"

    # Same itinerary, different idempotency key -> real 409 conflict.
    second = create_booking(payload, str(uuid.uuid4()))
    assert second.status_code == 409


def test_real_idempotency_key_returns_same_booking():

    traveler = f"SmokeTest-{uuid.uuid4()}"
    payload = {"traveler_name": traveler, "flight_id": 2, "hotel_id": 2}
    key = str(uuid.uuid4())

    first = create_booking(payload, key)
    assert first.status_code == 200

    # Same idempotency key -> same booking returned, NOT a 409.
    replay = create_booking(payload, key)
    assert replay.status_code == 200
    assert replay.json()["booking_id"] == first.json()["booking_id"]
