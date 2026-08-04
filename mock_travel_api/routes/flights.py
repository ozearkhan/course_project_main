from fastapi import APIRouter

from mock_travel_api.services.flight_service import search_flights

router = APIRouter(
    prefix="/flights",
    tags=["Flights"],
)


@router.get("/search")
def search(destination: str):

    flights = search_flights(destination)

    return {
        "count": len(flights),
        "results": flights,
    }