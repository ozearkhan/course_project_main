import os

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_ollama import ChatOllama

from tools.flight_tool import flight_tool
from tools.hotel_tool import hotel_tool
from tools.currency_tool import currency_tool
from tools.policy_tool import policy_tool

load_dotenv()

llm = ChatOllama(
    model=os.getenv("MODEL_NAME"),
    base_url=os.getenv("OLLAMA_BASE_URL"),
    temperature=0,
)

agent = create_agent(
    model=llm,
    tools=[
        flight_tool,
        hotel_tool,
        currency_tool,
        policy_tool,
    ],
)


def run_agent(query: str):

    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        }
    )

    return response


if __name__ == "__main__":

    while True:

        query = input("\nYou: ")

        if query.lower() == "exit":
            break

        response = run_agent(query)

        print("\nAssistant:\n")

        print(response)