from mock_travel_api.database import get_connection

print("flight_service.py loaded")


def search_flights(destination: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM flights
        WHERE LOWER(destination)=LOWER(?)
        ORDER BY price
        LIMIT 10
        """,
        (destination,),
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]