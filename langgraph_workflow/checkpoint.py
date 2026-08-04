from langgraph.checkpoint.sqlite import SqliteSaver

checkpointer_cm = SqliteSaver.from_conn_string(
    "tripilot_checkpoint.db"
)

memory = checkpointer_cm.__enter__()