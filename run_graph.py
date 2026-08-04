from dotenv import load_dotenv

load_dotenv()

from uuid import uuid4

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph_workflow.graph import builder

#thread_id = "trip-demo-001"
from uuid import uuid4

thread_id = str(uuid4())

print("Thread ID:", thread_id)

with SqliteSaver.from_conn_string("tripilot_checkpoint.db") as memory:

    graph = builder.compile(checkpointer=memory)

    config = {
        "configurable": {
            "thread_id": thread_id
        },
        "metadata": {
            "thread_id": thread_id
        },
    }

    state = {
        "traveler_name": "Amulya",
        "destination": "Paris",
        "budget": 1500,
    }

    result = graph.invoke(state, config=config)

    print(result)