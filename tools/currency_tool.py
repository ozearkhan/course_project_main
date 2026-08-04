import time
import requests

from logs.logger import log_tool_call

from pydantic import BaseModel, Field
from tenacity import retry, stop_after_attempt, wait_exponential
from langchain_core.tools import StructuredTool


BASE_URL = "http://127.0.0.1:8000"


class CurrencyInput(BaseModel):
    amount: float = Field(..., gt=0)
    from_currency: str = Field(..., min_length=3, max_length=3)
    to_currency: str = Field(..., min_length=3, max_length=3)


@retry(
    stop=stop_after_attempt(2),
    wait=wait_exponential(multiplier=1),
)
def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
):

    start = time.time()

    try:

        response = requests.get(
            f"{BASE_URL}/currency/convert",
            params={
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
            },
            timeout=5,
        )

        response.raise_for_status()

        result = response.json()

        log_tool_call(
            "convert_currency",
            {
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
            },
            "success",
            start,
        )

        return result

    except requests.Timeout:

        log_tool_call(
            "convert_currency",
            {
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
            },
            "timeout",
            start,
        )

        return {
            "error": "Request timed out."
        }

    except requests.HTTPError:

        log_tool_call(
            "convert_currency",
            {
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
            },
            "http_error",
            start,
        )

        return {
            "error": "Currency service returned an HTTP error."
        }

    except requests.RequestException:

        log_tool_call(
            "convert_currency",
            {
                "amount": amount,
                "from_currency": from_currency,
                "to_currency": to_currency,
            },
            "request_error",
            start,
        )

        return {
            "error": "Unable to contact currency service."
        }


currency_tool = StructuredTool.from_function(
    func=convert_currency,
    name="convert_currency",
    description="Convert one currency into another.",
    args_schema=CurrencyInput,
)