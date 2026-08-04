import re

SQL_KEYWORDS = [
    "flight",
    "flights",
    "hotel",
    "hotels",
    "price",
    "prices",
    "cost",
    "fare",
    "available",
    "availability",
    "seat",
    "seats",
    "room",
    "rooms",
    "book",
    "booking",
    "cheapest",
    "expensive",
]


def route_query(question: str) -> str:

    question = question.lower()

    for keyword in SQL_KEYWORDS:
        if re.search(rf"\b{re.escape(keyword)}\b", question):
            return "sqlite"

    return "rag"