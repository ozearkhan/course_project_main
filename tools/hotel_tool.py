import time
import requests

from logs.logger import log_tool_call

from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain_core.tools import StructuredTool


BASE_URL = "http://127.0.0.1:8000"


class HotelInput(BaseModel):
    city: str = Field(..., min_length=1)


@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=1),
)
def search_hotels(city: str):

    start = time.time()

    try:

        response = requests.get(
            f"{BASE_URL}/hotels/search",
            params={
                "city": city
            },
            timeout=5,
        )

        response.raise_for_status()

        result = response.json()

        log_tool_call(
            "search_hotels",
            {"city": city},
            "success",
            start,
        )

        return result

    except requests.Timeout:

        log_tool_call(
            "search_hotels",
            {"city": city},
            "timeout",
            start,
        )

        return {
            "error": "Request timed out."
        }

    except requests.HTTPError:

        log_tool_call(
            "search_hotels",
            {"city": city},
            "http_error",
            start,
        )

        return {
            "error": "Hotel service returned an HTTP error."
        }

    except requests.RequestException:

        log_tool_call(
            "search_hotels",
            {"city": city},
            "request_error",
            start,
        )

        return {
            "error": "Unable to contact hotel service."
        }


hotel_tool = StructuredTool.from_function(
    func=search_hotels,
    name="search_hotels",
    description="Search available hotels by city.",
    args_schema=HotelInput,
)