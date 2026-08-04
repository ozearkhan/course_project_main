import requests

BASE_URL = "http://127.0.0.1:8000"


def create_booking(
    booking_data: dict,
    idempotency_key: str,
):

    headers = {
        "Idempotency-Key": idempotency_key
    }

    response = requests.post(
        f"{BASE_URL}/bookings",
        json=booking_data,
        headers=headers,
        timeout=5,
    )

    return response