exchange_rates = {
    "USD": 1.0,
    "EUR": 0.92,
    "INR": 86.5,
    "JPY": 148.3,
    "GBP": 0.78,
}


def convert_currency(amount: float, from_currency: str, to_currency: str):

    from_currency = from_currency.upper()
    to_currency = to_currency.upper()

    if from_currency not in exchange_rates:
        raise ValueError(f"Unsupported currency: {from_currency}")

    if to_currency not in exchange_rates:
        raise ValueError(f"Unsupported currency: {to_currency}")

    usd_amount = amount / exchange_rates[from_currency]
    converted_amount = usd_amount * exchange_rates[to_currency]

    return {
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
        "converted_amount": round(converted_amount, 2),
    }