from mcp.server.fastmcp import FastMCP

from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels
from langgraph_workflow.booking_service import create_booking

mcp = FastMCP("TripPilot MCP Server")


# --------------------------------------------------
# Flight Search
# --------------------------------------------------

@mcp.tool()
def search_flights_tool(destination: str):

    return search_flights(destination)


# --------------------------------------------------
# Hotel Search
# --------------------------------------------------

@mcp.tool()
def search_hotels_tool(city: str):

    return search_hotels(city)


# --------------------------------------------------
# Booking
# --------------------------------------------------

@mcp.tool()
def create_booking_tool(payload: dict, idempotency_key: str):

    response = create_booking(
        payload,
        idempotency_key
    )

    return response.json()


# --------------------------------------------------
# Currency Conversion
# --------------------------------------------------

FX_RATES = {
    "USD": 1.0,
    "EUR": 1.08,
    "GBP": 1.28,
    "INR": 0.012,
    "AED": 0.27,
    "SGD": 0.74,
}


@mcp.tool()
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
):

    usd = amount * FX_RATES[from_currency]

    converted = usd / FX_RATES[to_currency]

    return round(converted, 2)


# --------------------------------------------------
# Policy Tool
# --------------------------------------------------

@mcp.tool()
def get_policy(policy_name: str):

    policies = {
        "refund": "Refund allowed within 24 hours.",
        "baggage": "One checked bag included.",
        "visa": "Passport validity must exceed 6 months.",
    }

    return policies.get(
        policy_name.lower(),
        "Policy not found.",
    )


if __name__ == "__main__":

    mcp.run()