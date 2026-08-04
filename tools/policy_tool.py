import time

from logs.logger import log_tool_call

from pydantic import BaseModel, Field
from langchain_core.tools import StructuredTool

from rag_service import get_policy_answer


class PolicyInput(BaseModel):
    question: str = Field(..., min_length=3)


def get_policy(question: str):

    start = time.time()

    try:

        result = get_policy_answer(question)

        log_tool_call(
            "get_policy",
            {
                "question": question
            },
            "success",
            start,
        )

        return result

    except Exception:

        log_tool_call(
            "get_policy",
            {
                "question": question
            },
            "failure",
            start,
        )

        return {
            "error": "Unable to retrieve travel policy."
        }


policy_tool = StructuredTool.from_function(
    func=get_policy,
    name="get_policy",
    description="Answer travel policy questions using the TripPilot knowledge base.",
    args_schema=PolicyInput,
)