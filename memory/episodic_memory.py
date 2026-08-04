import sqlite3

DATABASE = "seed/travel.db"


def save_trip(
    traveler_name: str,
    destination: str,
    hotel_name: str,
    flight_airline: str,
    total_cost: float,
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO traveler_history(
            traveler_name,
            destination,
            hotel_name,
            flight_airline,
            total_cost
        )
        VALUES(?,?,?,?,?)
        """,
        (
            traveler_name,
            destination,
            hotel_name,
            flight_airline,
            total_cost,
        ),
    )

    conn.commit()
    conn.close()


def load_trip_history(traveler_name: str):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM traveler_history
        WHERE traveler_name = ?
        ORDER BY booked_at DESC
        """,
        (traveler_name,),
    )

    rows = cursor.fetchall()

    conn.close()

    return [dict(row) for row in rows]