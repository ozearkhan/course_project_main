-- ==========================================
-- Flights
-- ==========================================

DROP TABLE IF EXISTS flights;

CREATE TABLE flights (
    flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
    airline TEXT NOT NULL,
    origin TEXT NOT NULL,
    destination TEXT NOT NULL,
    departure_date DATE NOT NULL,
    departure_time TEXT NOT NULL,
    arrival_time TEXT NOT NULL,
    duration_minutes INTEGER NOT NULL,
    price REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    seats_available INTEGER NOT NULL,
    status TEXT DEFAULT 'AVAILABLE'
);

-- ==========================================
-- Hotels
-- ==========================================

DROP TABLE IF EXISTS hotels;

CREATE TABLE hotels (
    hotel_id INTEGER PRIMARY KEY AUTOINCREMENT,
    hotel_name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    star_rating INTEGER,
    price_per_night REAL NOT NULL,
    currency TEXT DEFAULT 'USD',
    rooms_available INTEGER NOT NULL,
    refundable INTEGER DEFAULT 1,
    amenities TEXT
);

-- ==========================================
-- Travelers
-- ==========================================

DROP TABLE IF EXISTS travelers;

CREATE TABLE travelers (
    traveler_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT UNIQUE,
    passport_number TEXT,
    nationality TEXT
);

-- ==========================================
-- Bookings
-- ==========================================

DROP TABLE IF EXISTS bookings;

CREATE TABLE bookings (
    booking_id INTEGER PRIMARY KEY AUTOINCREMENT,
    traveler_id INTEGER,
    booking_type TEXT,
    reference_id INTEGER,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    total_amount REAL,
    currency TEXT DEFAULT 'USD',
    status TEXT DEFAULT 'CONFIRMED',

    FOREIGN KEY (traveler_id)
        REFERENCES travelers(traveler_id)
);

-- ==========================================
-- Exchange Rates
-- ==========================================

DROP TABLE IF EXISTS fx_rates;

CREATE TABLE fx_rates (
    currency_code TEXT PRIMARY KEY,
    exchange_rate_to_usd REAL NOT NULL,
    last_updated DATE
);

-- ==========================================
-- Module 5 : Semantic Memory
-- ==========================================

DROP TABLE IF EXISTS traveler_prefs;

CREATE TABLE traveler_prefs (
    traveler_name TEXT PRIMARY KEY,
    budget_band TEXT,
    seat_preference TEXT,
    hotel_preference TEXT,
    dietary_notes TEXT
);

-- ==========================================
-- Module 5 : Episodic Memory
-- ==========================================

DROP TABLE IF EXISTS traveler_history;

CREATE TABLE traveler_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    traveler_name TEXT NOT NULL,
    destination TEXT NOT NULL,
    hotel_name TEXT,
    flight_airline TEXT,
    total_cost REAL,
    booked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);