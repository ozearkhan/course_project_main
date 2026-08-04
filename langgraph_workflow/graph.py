from langgraph.graph import StateGraph, START, END
from langgraph_workflow.checkpoint import memory
from langgraph_workflow.state import TripState
from langgraph_workflow.nodes import (
    collect_requirements,
    search,
    assemble_itinerary,
    budget_check,
    present_options,
    execute_booking,
    confirm,
    budget_router,
    approval_router,
    booking_router,
)
from langgraph_workflow.memory_nodes import load_traveler_context

builder = StateGraph(TripState)

builder.add_node("collect_requirements", collect_requirements)
builder.add_node(
    "load_traveler_context",
    load_traveler_context,
)
builder.add_node("search", search)
builder.add_node("assemble_itinerary", assemble_itinerary)
builder.add_node("budget_check", budget_check)
builder.add_node("present_options", present_options)
builder.add_node("execute_booking", execute_booking)
builder.add_node("confirm", confirm)

builder.add_edge(START, "collect_requirements")

builder.add_edge(
    "collect_requirements",
    "load_traveler_context",
)

builder.add_edge(
    "load_traveler_context",
    "search",
)
builder.add_edge("search", "assemble_itinerary")
builder.add_edge("assemble_itinerary", "budget_check")

builder.add_conditional_edges(
    "budget_check",
    budget_router,
    {
        "within_budget": "present_options",
        "revise": "search",
        "budget_failed": END,
    },
)
builder.add_conditional_edges(
    "present_options",
    approval_router,
    {
        "approved": "execute_booking",
        "rejected": END,
    },
)
builder.add_conditional_edges(
    "execute_booking",
    booking_router,
    {
        "confirmed": "confirm",
        "retry": "search",
    },
)



builder.add_edge("confirm", END)

graph = builder.compile(
    checkpointer=memory
)