from fastapi import APIRouter, HTTPException

from mock_travel_api.services.currency_service import convert_currency

router = APIRouter(
    prefix="/currency",
    tags=["Currency"],
)


@router.get("/convert")
def convert(
    amount: float,
    from_currency: str,
    to_currency: str,
):

    try:
        return convert_currency(
            amount,
            from_currency,
            to_currency,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )