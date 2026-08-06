# ✈️ TripPilot AI - Intelligent Travel Planning Assistant

TripPilot AI is an AI-powered travel assistant that helps users plan and book trips using a combination of Retrieval-Augmented Generation (RAG), Model Context Protocol (MCP), LangGraph workflows, Human-in-the-Loop (HITL) approvals, and long-term memory.

The project demonstrates how modern AI applications can orchestrate multiple tools, maintain user context, retrieve domain knowledge, and execute bookings through a structured workflow.

---

# Features

- AI-powered travel itinerary planning
- Flight search
- Hotel search
- Human approval before booking
- LangGraph workflow orchestration
- MCP (Model Context Protocol) server & client
- RAG-powered travel knowledge retrieval
- Semantic Memory
- Episodic Memory
- Budget validation
- Booking execution
- Idempotent booking requests
- SQLite-backed storage
- Mock Travel REST API
- Guardrails & Validation
- Comprehensive Pytest test suite

---

# Architecture

```
                    ┌───────────────────────────┐
                    │        User Request       │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                     Collect User Requirements
                                  │
                                  ▼
                     Load Traveler Memory
                 (Semantic + Episodic Memory)
                                  │
                                  ▼
                        MCP Tool Invocation
                    ┌─────────────┴─────────────┐
                    │                           │
                    ▼                           ▼
             Flight Search                Hotel Search
                    │                           │
                    └─────────────┬─────────────┘
                                  ▼
                        Assemble Itinerary
                                  │
                                  ▼
                          Budget Validation
                                  │
                                  ▼
                     Human Approval (Interrupt)
                                  │
                  ┌───────────────┴───────────────┐
                  │                               │
              Approved                      Rejected
                  │                               │
                  ▼                               ▼
           Execute Booking                 Search Again
                  │
                  ▼
           Booking Confirmation
```

---

# Tech Stack

- Python 3.10+
- LangGraph
- LangChain
- MCP (Model Context Protocol)
- FastAPI
- ChromaDB
- SQLite
- Pydantic
- Pytest
- AnyIO
- Requests

---

# Project Structure

```
course_project/
│
├── langgraph_workflow/
│   ├── graph.py
│   ├── nodes.py
│   ├── state.py
│   ├── approval.py
│   ├── checkpoint.py
│   ├── booking_service.py
│   ├── memory_nodes.py
│   └── constants.py
│
├── memory/
│   ├── episodic_memory.py
│   ├── semantic_memory.py
│   └── memory_service.py
│
├── mcp_server/
│   ├── server.py
│   └── mcp_tools.py
│
├── mock_travel_api/
│
├── tools/
│
├── seed/
│
├── tests/
│
├── app.py
├── rag_service.py
├── mcp_client.py
├── run_graph.py
├── resume_graph.py
├── ingest.py
└── requirements.txt
```

---

# Workflow

The application follows this execution flow:

1. Collect traveler requirements
2. Load traveler preferences & history
3. Search flights
4. Search hotels
5. Assemble itinerary
6. Validate budget
7. Request human approval
8. Execute booking
9. Save trip memory
10. Return booking confirmation

---

# Memory

## Semantic Memory

Stores long-term traveler preferences such as:

- Seat preference
- Hotel preference
- Budget band
- Dietary preferences

Example:

```
Window seat
4-star hotels
Standard budget
```

---

## Episodic Memory

Stores previous trips.

Example:

```
Paris
Stayed at Paris Grand Hotel
Booked Emirates
```

This information is automatically loaded before planning a new trip.

---

# RAG

TripPilot includes a Retrieval-Augmented Generation pipeline using ChromaDB.

Travel-related documents are embedded into a vector database and retrieved during user queries.

Knowledge includes topics such as:

- Visa
- Destinations
- Booking policies
- Travel guidelines

To build the vector database:

```bash
python ingest.py
```

---

# MCP (Model Context Protocol)

The project exposes travel capabilities as MCP tools.

Available tools:

| Tool | Description |
|------|-------------|
| search_flights_tool | Search available flights |
| search_hotels_tool | Search available hotels |
| create_booking_tool | Create booking |
| convert_currency | Currency conversion |
| get_policy | Retrieve travel policies |

---

# Human-in-the-Loop (HITL)

Before booking, the workflow pauses for human approval.

Possible outcomes:

- Approve itinerary
- Reject itinerary
- Retry with another itinerary (booking conflict)

This is implemented using LangGraph interrupts.

---

# Mock Travel API

A FastAPI service simulates:

- Flights
- Hotels
- Bookings
- Currency
- Travel data

Run the API:

```bash
uvicorn mock_travel_api.main:app --reload
```

---

# Installation

Clone the repository:

```bash
git clone https://github.com/Amulyagangishetti/course_project.git

cd course_project
```

Create virtual environment:

```bash
python -m venv .venv
```

Activate:

Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Copy `.env.example` to `.env` and fill in your real values (`.env` is gitignored):

```bash
cp .env.example .env
```

```
MODEL_NAME=<ollama model tag, e.g. llama3.1:8b>
OLLAMA_BASE_URL=<ollama server url, e.g. http://localhost:11434>
CHROMA_DB=<path to persistent Chroma directory>
DOCUMENT_PATH=<path to seed docs, e.g. ./seed/docs>

LANGSMITH_TRACING=true
LANGSMITH_API_KEY=<your LangSmith API key>
LANGSMITH_PROJECT=trippilot

JUDGE_MODEL_NAME=<a different Ollama model than MODEL_NAME, e.g. qwen2.5:7b - used only as the generation-eval judge>
```

`LANGSMITH_*` vars enable tracing to LangSmith (see Evaluation & Observability
below) — the app runs fine without them, tracing is simply skipped.

Ollama itself is a separate runtime, not a pip package, so it isn't in
`requirements.txt`. Install it from [ollama.com](https://ollama.com), then
pull both models:

```bash
ollama pull llama3.1:8b
ollama pull qwen2.5:7b
```

---

# Running the Project

### 1. Build Vector Database

```bash
python ingest.py
```

---

### 2. Start Mock Travel API

```bash
uvicorn mock_travel_api.main:app --reload
```

---

### 3. Run the LangGraph Workflow

```bash
python run_graph.py
```

---

### 4. Resume After Human Approval

`run_graph.py` prints a `Thread ID` and pauses at the approval interrupt. Pass
that same ID to `resume_graph.py` to resume that exact conversation:

```bash
python resume_graph.py <thread_id>
```

---

# Testing

Run the complete test suite:

```bash
python -m pytest
```

Current Status:

```
19 tests passed
```

Test coverage includes:

- Agent
- LangGraph Workflow
- Validation
- Guardrails
- Timeout Handling
- SQLite
- RAG
- Router

---

# Current Capabilities

✔ Retrieval-Augmented Generation (RAG)

✔ Model Context Protocol (MCP)

✔ LangGraph Workflow

✔ Human-in-the-Loop Approval

✔ Semantic Memory

✔ Episodic Memory

✔ Budget Validation

✔ Booking Execution

✔ SQLite Persistence

✔ FastAPI Mock Services

✔ Unit Testing

---

# Future Enhancements

- LangSmith Observability
- Multi-agent Planner
- Real Flight APIs
- Real Hotel APIs
- Authentication
- User Dashboard
- Streaming Responses
- Multi-language Support

---


AI • Python • LangGraph • MCP • RAG • Generative AI