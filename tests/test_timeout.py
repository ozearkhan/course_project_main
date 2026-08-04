from tools.flight_tool import flight_tool


def test_timeout():
    response = flight_tool.invoke(
        {
            "destination": "Paris"
        }
    )

    assert response is not None