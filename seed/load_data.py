import sqlite3
import random
from pathlib import Path
from datetime import datetime, timedelta

BASE_DIR = Path(__file__).parent

DB_PATH = BASE_DIR / "travel.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# ----------------------------------------------------
# Create Tables
# ----------------------------------------------------

with open(SCHEMA_PATH, "r") as f:
    cursor.executescript(f.read())

# ----------------------------------------------------
# Sample Data
# ----------------------------------------------------

AIRLINES = [
    "Emirates",
    "Qatar Airways",
    "Singapore Airlines",
    "Lufthansa",
    "Air India",
    "British Airways",
    "IndiGo",
    "Etihad"
]

DESTINATIONS = [
    ("New York", "USA"),
    ("Paris", "France"),
    ("Tokyo", "Japan"),
    ("Dubai", "UAE"),
    ("Singapore", "Singapore"),
    ("London", "UK"),
    ("Sydney", "Australia"),
    ("Rome", "Italy"),
    ("Bangkok", "Thailand"),
    ("Bali", "Indonesia"),
    ("Zurich", "Switzerland"),
    ("Barcelona", "Spain")
]

AMENITIES = [
    "Free WiFi,Gym,Pool",
    "Breakfast,Parking",
    "Spa,Pool,Gym",
    "Airport Shuttle",
    "Beach Access",
    "Business Lounge",
    "Restaurant,Bar",
    "Free WiFi,Breakfast"
]

# ----------------------------------------------------
# Flights
# ----------------------------------------------------

today = datetime.today()

for _ in range(200):

    origin = random.choice(DESTINATIONS)

    destination = random.choice(DESTINATIONS)

    while destination == origin:
        destination = random.choice(DESTINATIONS)

    travel_day = today + timedelta(days=random.randint(1, 180))

    departure_hour = random.randint(0, 23)

    departure_min = random.choice([0, 15, 30, 45])

    duration = random.randint(60, 900)

    departure_datetime = datetime.combine(
            travel_day.date(),
            datetime.min.time()
        )+ timedelta(
            hours=departure_hour,
            minutes=departure_min
        )
    arrival = departure_datetime + timedelta(minutes=duration)
    

    seats = random.randint(0, 180)

    status = "AVAILABLE"

    if seats == 0:
        status = "SOLD_OUT"

    cursor.execute(
        """
        INSERT INTO flights(
            airline,
            origin,
            destination,
            departure_date,
            departure_time,
            arrival_time,
            duration_minutes,
            price,
            seats_available,
            status
        )
        VALUES(?,?,?,?,?,?,?,?,?,?)
        """,
        (
            random.choice(AIRLINES),
            origin[0],
            destination[0],
            travel_day.date(),
            f"{departure_hour:02}:{departure_min:02}",
            arrival.strftime("%H:%M"),
            duration,
            round(random.uniform(120, 1800), 2),
            seats,
            status
        )
    )

# ----------------------------------------------------
# Hotels
# ----------------------------------------------------

for city, country in DESTINATIONS:

    for i in range(5):

        cursor.execute(
            """
            INSERT INTO hotels(
                hotel_name,
                city,
                country,
                star_rating,
                price_per_night,
                rooms_available,
                refundable,
                amenities
            )
            VALUES(?,?,?,?,?,?,?,?)
            """,
            (
                f"{city} Grand Hotel {i+1}",
                city,
                country,
                random.randint(3, 5),
                round(random.uniform(80, 650), 2),
                random.randint(0, 80),
                random.randint(0, 1),
                random.choice(AMENITIES)
            )
        )

# ----------------------------------------------------
# Exchange Rates
# ----------------------------------------------------

fx = [
    ("USD", 1.0),
    ("EUR", 1.08),
    ("GBP", 1.28),
    ("JPY", 0.0068),
    ("INR", 0.012),
    ("AED", 0.27),
    ("SGD", 0.74),
    ("AUD", 0.67)
]

for code, rate in fx:

    cursor.execute(
        """
        INSERT INTO fx_rates
        VALUES(?,?,?)
        """,
        (
            code,
            rate,
            datetime.today().date()
        )
    )
# ----------------------------------------------------

# Edge Cases

# ----------------------------------------------------

# Sold out flight

cursor.execute("""

UPDATE flights

SET seats_available = 0,

    status = 'SOLD_OUT'

WHERE flight_id = 1;

""")

# Only one seat left

cursor.execute("""

UPDATE flights

SET seats_available = 1

WHERE flight_id = 2;

""")

# Premium flight (price outlier)

cursor.execute("""

UPDATE flights

SET price = 4999.99

WHERE flight_id = 3;

""")

# Budget flight (price outlier)

cursor.execute("""

UPDATE flights

SET price = 49.99

WHERE flight_id = 4;

""")

# Sold out hotel

cursor.execute("""

UPDATE hotels

SET rooms_available = 0

WHERE hotel_id = 1;

""")
conn.commit()
conn.close()

print("=" * 60)
print("Travel database created successfully.")
print(f"Location : {DB_PATH}")
print("Flights   : 200")
print("Hotels    : 60")
print("FX Rates  :", len(fx))
print("=" * 60)