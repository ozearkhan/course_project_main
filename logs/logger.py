import json
import os
import time


LOG_FILE = "logs/tool_calls.jsonl"


def log_tool_call(
    tool_name,
    arguments,
    outcome,
    start_time,
):

    os.makedirs("logs", exist_ok=True)

    latency = round(
        time.time() - start_time,
        3,
    )

    entry = {
        "tool": tool_name,
        "args": arguments,
        "latency": latency,
        "outcome": outcome,
    }

    with open(
        LOG_FILE,
        "a",
        encoding="utf-8",
    ) as file:

        file.write(
            json.dumps(entry)
            + "\n"
        )