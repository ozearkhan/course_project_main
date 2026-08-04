from sqlite_service import get_sql_response


def test_flights():

    response = get_sql_response(
        "Show me flights to Paris"
    )

    assert "AVAILABLE FLIGHTS" in response


def test_hotels():

    response = get_sql_response(
        "Show me hotels in Tokyo"
    )

    assert "AVAILABLE HOTELS" in response


def test_invalid():

    response = get_sql_response(
        "Show me trains"
    )

    assert "couldn't understand" in response.lower()