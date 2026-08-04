import requests

from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain_core.tools import StructuredTool

BASE_URL = "http://127.0.0.1:8000"

class FlightInput(BaseModel):
    destination: str = Field(..., min_length=1)

@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=1),
)
def search_flights(destination: str):

    try:

        response = requests.get(
            f"{BASE_URL}/flights/search",
            params={"destination": destination},
            timeout=5,
        )

        response.raise_for_status()

        return response.json()

    except requests.Timeout:
        return {"error": "Request timed out."}

    except requests.HTTPError:
        return {"error": "Flight service returned an HTTP error."}

    except requests.RequestException:
        return {"error": "Unable to contact flight service."}
flight_tool = StructuredTool.from_function(
    func=search_flights,
    name="search_flights",
    description="Search available flights by destination.",
    args_schema=FlightInput,
)