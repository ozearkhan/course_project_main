from fastapi import APIRouter

from mock_travel_api.services.hotel_service import search_hotels

router = APIRouter(
    prefix="/hotels",
    tags=["Hotels"],
)


@router.get("/search")
def search(city: str):

    hotels = search_hotels(city)

    return {
        "count": len(hotels),
        "results": hotels,
    }