from dotenv import load_dotenv

load_dotenv()

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from langgraph_workflow.graph import builder

thread_id = "trip-demo-001"

with SqliteSaver.from_conn_string("tripilot_checkpoint.db") as memory:

    graph = builder.compile(
        checkpointer=memory
    )

    config = {
        "configurable": {
            "thread_id": thread_id
        },
        "metadata": {
            "thread_id": thread_id
        },
    }

    approval = input(
        "Approve itinerary? (yes/no): "
    ).strip().lower()

    if approval == "yes":
        decision = {
            "status": "approved"
        }

    else:

        decision = {
            "status": "rejected"
        }

    result = graph.invoke(
        Command(resume=decision),
        config=config,
    )

    print(result)