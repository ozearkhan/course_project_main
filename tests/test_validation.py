import pytest

from tools.currency_tool import convert_currency


def test_validation():

    with pytest.raises(Exception):

        convert_currency.invoke(
            {
                "amount": -10,
                "from_currency": "USD",
                "to_currency": "INR",
            }
        )