import sqlite3

DATABASE = "seed/travel.db"


def load_preferences(traveler_name: str):

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM traveler_prefs
        WHERE traveler_name = ?
        """,
        (traveler_name,),
    )

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return dict(row)


def save_preferences(
    traveler_name: str,
    budget_band: str,
    seat_preference: str,
    hotel_preference: str,
    dietary_notes: str,
):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO traveler_prefs(
            traveler_name,
            budget_band,
            seat_preference,
            hotel_preference,
            dietary_notes
        )
        VALUES(?,?,?,?,?)
        """,
        (
            traveler_name,
            budget_band,
            seat_preference,
            hotel_preference,
            dietary_notes,
        ),
    )

    conn.commit()
    conn.close()