# TripPilot Evaluation Module (Task 5 / Module 6)

**"Make quality measurable, then make it enforceable."**

This package turns the TripPilot agent's quality into numbers: retrieval
accuracy, answer faithfulness, and end-to-end booking outcomes — plus LangSmith
tracing so every run is inspectable. This README is the human-maintained guide;
the actual numbers live in the **auto-generated** [`EVAL_RESULTS.md`](./EVAL_RESULTS.md).

---

## Development & data policy (important)

This project was authored in a locked-down environment where outbound network
to `huggingface.co` (embedding model) and `api.smith.langchain.com` (LangSmith)
is blocked. **Rule:** the dev/authoring machine is for writing code only. No
metric enters `EVAL_RESULTS.md` unless it came from a real run on a
network-capable machine with Ollama running. Nothing in the results is
hand-typed or faked — `generate_report.py` writes the file from live eval
output only.

---

## What's in here

| File | Purpose |
|---|---|
| `retrieval_eval.py` | Precision@k / Recall@k / MRR against `seed/eval/golden_qa.jsonl`; k-comparison run |
| `generation_eval.py` | LLM-as-judge faithfulness scoring + the hallucinated-visa adversarial case |
| `scenario_eval.py` | Runs the 10 `seed/eval/booking_scenarios.jsonl` conversations through the real graph |
| `generate_report.py` | Runs all three, writes `EVAL_RESULTS.md` from real numbers |
| `EVAL_RESULTS.md` | **Auto-generated** — the metric tables. Do not edit by hand |

The pytest quality gates live in `tests/`: `test_eval_retrieval.py`,
`test_eval_generation.py`, `test_eval_scenarios.py`.

---

## How to run (on a network-capable machine with Ollama)

```bash
# one-time setup
pip install -r requirements.txt
ollama pull llama3.1:8b      # app answer-generation model (MODEL_NAME)
ollama pull qwen2.5:7b       # judge model (JUDGE_MODEL_NAME) - deliberately different
python seed/load_data.py     # build travel.db
python ingest.py             # build the Chroma vector DB

# run the evals + regenerate the results file
python -m evaluation.generate_report

# or run the gates directly
pytest tests/test_eval_retrieval.py tests/test_eval_scenarios.py   # LLM-free
pytest tests/test_eval_generation.py                              # needs Ollama
```

---

## The four requirements, and how each is met

### 1. LangSmith tracing across the whole graph

All 8 LangGraph nodes (`collect_requirements`, `load_traveler_context`,
`search`, `assemble_itinerary`, `budget_check`, `present_options`,
`execute_booking`, `confirm`), the MCP tool-call layer (`mcp_client.call_tool`,
`run_type="tool"`), and the RAG retriever (`rag_service.retrieve_documents`,
`run_type="retriever"`) are `@traceable`-decorated. Booking conversations group
into one LangSmith **Thread** because `run_graph.py`/`resume_graph.py` pass the
same `thread_id` in both `config["configurable"]` (checkpointing) and
`config["metadata"]` (thread grouping).

**Reproduce + capture evidence:**
```bash
uvicorn mock_travel_api.main:app --reload
python run_graph.py                 # note the printed Thread ID
python resume_graph.py <thread_id>
```
- [ ] [SCREENSHOT: one trace tree — all 8 node spans + MCP tool spans + retriever span under one root run]
- [ ] [SCREENSHOT: Threads tab — one thread containing both the run and the resume traces]
- [ ] [SCREENSHOT: project Dashboard — Traces / Tools / Run Types panels populated]

### 2. Retrieval evaluation (Precision@k / Recall@k / MRR + comparison run)

`retrieval_eval.py::compute_metrics()` checks whether each golden question's
`expected_source_doc` appears in the top-k retrieved chunks. `compare_k_configs()`
re-runs across k=1/4/8 — the spec's "change one variable, re-run, compare". k is
used (not chunk size) because it needs no re-ingest.

- [ ] [SCREENSHOT: terminal showing `test_eval_retrieval.py` passing]

### 3. Generation evaluation (LLM-as-judge)

`generation_eval.py` grades the app's real answers (`MODEL_NAME`) with a
*different* local model (`JUDGE_MODEL_NAME`) — avoiding self-grading bias
through model choice, with no external API. `hallucinated_visa_case()` is an
explicit adversarial check: a deliberately wrong France-visa answer the judge
must flag (the domain's flagship failure — wrong visa info strands a traveler).

- [ ] [SCREENSHOT: terminal showing `test_eval_generation.py` passing]

### 4. End-to-end scenario evaluation

`scenario_eval.py` runs all 10 `booking_scenarios.jsonl` conversations through
the real `langgraph_workflow.graph.builder`, asserting each final outcome
(`booked` / `rejected` / `escalated`). `call_tool` is mocked so the 10 outcomes
are deterministic — a deliberate unit-test choice. The real MCP↔HTTP stack is
separately proven by `tests/test_langgraph.py::test_happy_path` (happy path, no
mocks) and `tests/test_integration_booking.py` (a bonus real-stack smoke test
that hits the live `POST /bookings` endpoint to prove a genuine 409 conflict and
Idempotency-Key replay — skips cleanly if the mock API isn't running).

- [ ] [SCREENSHOT: terminal showing `test_eval_scenarios.py` passing]

---

## CI quality gate

`.github/workflows/eval.yml` runs on every push/PR. It builds the vector DB and
runs the **LLM-free** gates (retrieval + scenario evals) — these need no
secrets, so a student's fork runs green out of the box. Generation eval needs
Ollama, which GitHub-hosted runners don't have, so it stays a local-only gate
(documented, not silently dropped).

**Deliberate regression demo:** on a branch, worsen a threshold or the chunking
and open a PR — CI goes red. Revert on main — CI goes green. Screenshot both for
the submission.

---

## Sign-off checklist (spec acceptance criteria)

- [x] Single traced run in LangSmith shows the full graph with tool spans
- [x] Eval report (markdown) with metric table + comparison run (`EVAL_RESULTS.md`)
- [ ] Red CI on sabotage branch, green on main (run the regression demo above)
