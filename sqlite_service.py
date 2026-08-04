import sqlite3
from pathlib import Path

DB_PATH = Path("seed/travel.db")


# ==========================================================
# Formatting Helpers
# ==========================================================

def format_flights(rows):
    if not rows:
        return "No matching flights found."

    response = ["✈️ AVAILABLE FLIGHTS\n"]

    for index, row in enumerate(rows, start=1):
        response.append(
            f"""
Flight {index}
----------------------------------------
Airline          : {row["airline"]}
Origin           : {row["origin"]}
Destination      : {row["destination"]}
Departure Date   : {row["departure_date"]}
Departure Time   : {row["departure_time"]}
Arrival Time     : {row["arrival_time"]}
Price            : {row["price"]:.2f} {row["currency"]}
Seats Available  : {row["seats_available"]}
Status           : {row["status"]}
"""
        )

    return "\n".join(response)


def format_hotels(rows):
    if not rows:
        return "No matching hotels found."

    response = ["🏨 AVAILABLE HOTELS\n"]

    for index, row in enumerate(rows, start=1):
        response.append(
            f"""
Hotel {index}
----------------------------------------
Hotel Name       : {row["hotel_name"]}
City             : {row["city"]}
Country          : {row["country"]}
Star Rating      : {row["star_rating"]}
Price / Night    : {row["price_per_night"]:.2f} {row["currency"]}
Rooms Available  : {row["rooms_available"]}
Refundable       : {"Yes" if row["refundable"] else "No"}
Amenities        : {row["amenities"]}
"""
        )

    return "\n".join(response)


# ==========================================================
# SQL Query Handler
# ==========================================================

def get_sql_response(question: str):

    question = question.lower()

    cities = [
        "paris",
        "tokyo",
        "london",
        "dubai",
        "bali",
        "singapore",
        "new york",
        "rome",
        "sydney",
    ]

    city = None

    for c in cities:
        if c in question:
            city = c.title()
            break

    try:

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        # ==================================================
        # Flights
        # ==================================================

        if "flight" in question or "flights" in question:

            if city:

                cursor.execute(
                    """
                    SELECT
                        airline,
                        origin,
                        destination,
                        departure_date,
                        departure_time,
                        arrival_time,
                        price,
                        currency,
                        seats_available,
                        status
                    FROM flights
                    WHERE LOWER(destination) = LOWER(?)
                    ORDER BY price ASC
                    LIMIT 10
                    """,
                    (city,),
                )

            else:

                cursor.execute(
                    """
                    SELECT
                        airline,
                        origin,
                        destination,
                        departure_date,
                        departure_time,
                        arrival_time,
                        price,
                        currency,
                        seats_available,
                        status
                    FROM flights
                    ORDER BY price ASC
                    LIMIT 10
                    """
                )

            rows = cursor.fetchall()

            return format_flights(rows)

        # ==================================================
        # Hotels
        # ==================================================

        if "hotel" in question or "hotels" in question:

            if city:

                cursor.execute(
                    """
                    SELECT
                        hotel_name,
                        city,
                        country,
                        star_rating,
                        price_per_night,
                        currency,
                        rooms_available,
                        refundable,
                        amenities
                    FROM hotels
                    WHERE LOWER(city) = LOWER(?)
                    ORDER BY price_per_night ASC
                    LIMIT 10
                    """,
                    (city,),
                )

            else:

                cursor.execute(
                    """
                    SELECT
                        hotel_name,
                        city,
                        country,
                        star_rating,
                        price_per_night,
                        currency,
                        rooms_available,
                        refundable,
                        amenities
                    FROM hotels
                    ORDER BY price_per_night ASC
                    LIMIT 10
                    """
                )

            rows = cursor.fetchall()

            return format_hotels(rows)

        return "I couldn't understand the SQL request."

    except sqlite3.Error as e:
        return f"Database Error: {e}"

    finally:
        if "conn" in locals():
            conn.close()