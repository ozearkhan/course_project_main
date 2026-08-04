from mock_travel_api.database import get_connection


def search_hotels(city: str):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM hotels
        WHERE LOWER(city)=LOWER(?)
        ORDER BY price_per_night
        LIMIT 10
        """,
        (city,),
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]
