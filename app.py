import os

from dotenv import load_dotenv

from router import route_query
from sqlite_service import get_sql_response
from pii_filter import mask_pii
from rag_service import get_policy_answer

load_dotenv()

DEBUG = True

print("\n🌍 TripPilot Travel Assistant")
print("Type 'exit' to quit.\n")

while True:

    question = input("You: ").strip()

    if question.lower() == "exit":
        print("\nThank you for using TripPilot!\n")
        break

    if not question:
        continue

    route = route_query(question)

    if DEBUG:
        print(f"\n[Router] -> {route}")

    if route == "sqlite":

        response = get_sql_response(question)

        response = mask_pii(response)

        print("\nAssistant:\n")
        print(response)
        print()

        continue

    response = get_policy_answer(question)

    print("\nAssistant:\n")
    print(response)
    print()