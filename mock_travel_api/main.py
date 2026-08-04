from fastapi import FastAPI

from mock_travel_api.routes.flights import router as flights_router
from mock_travel_api.routes.hotels import router as hotels_router
from mock_travel_api.routes.currency import router as currency_router
from mock_travel_api.routes.bookings import router as bookings_router

app = FastAPI(
    title="TripPilot Mock Travel API",
    version="1.0.0",
    description="Mock Travel API used by LangChain tools",
)

app.include_router(flights_router)
app.include_router(hotels_router)
app.include_router(currency_router)
app.include_router(bookings_router)


@app.get("/")
def root():
    return {
        "message": "TripPilot Mock Travel API is running."
    }