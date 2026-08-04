from router import route_query


def test_sql_route_flights():
    assert route_query("Show me flights to Paris") == "sqlite"


def test_sql_route_hotels():
    assert route_query("Show me hotels in Tokyo") == "sqlite"


def test_rag_route_visa():
    assert route_query("Do I need a visa for Japan?") == "rag"


def test_rag_route_policy():
    assert route_query("What is the baggage policy?") == "rag"