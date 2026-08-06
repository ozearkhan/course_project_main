# TripPilot — Task 5 Evaluation Report

This is the living evidence document for Task 5 (LangSmith tracing + evaluation).
Sections are filled in as each phase completes. Screenshots are marked with
`[SCREENSHOT NEEDED: ...]` — paste images from the LangSmith UI at those spots.

---

## 1. Tracing setup

- `LANGSMITH_TRACING=true`, `LANGSMITH_API_KEY`, `LANGSMITH_PROJECT=trippilot` configured via `.env`.
- All 7 LangGraph nodes (`collect_requirements`, `search`, `assemble_itinerary`, `budget_check`, `present_options`, `execute_booking`, `confirm`) explicitly decorated with `@traceable`.
- `mcp_client.call_tool` decorated `@traceable(run_type="tool")` — every MCP call (search_flights_tool, search_hotels_tool, create_booking_tool) appears as its own span.
- `rag_service.retrieve_documents` decorated `@traceable(run_type="retriever")`.
- `run_graph.py`/`resume_graph.py` pass the same `thread_id` in both `config["configurable"]` (LangGraph checkpointing) and `config["metadata"]` (LangSmith thread grouping).

**Verification (run on a machine with LangSmith network access):**

```powershell
python run_graph.py            # note the printed Thread ID
python resume_graph.py <thread_id>
```

Then in the LangSmith UI:

- [SCREENSHOT NEEDED: single trace tree showing nodes + tool spans + retriever span nested under one root run]
- [SCREENSHOT NEEDED: Threads tab showing one thread containing both the run_graph.py trace and the resume_graph.py trace grouped together]
- [SCREENSHOT NEEDED: prebuilt project Dashboard — Traces / Tools / Run Types panels populated]

---

## 2. Retrieval evaluation

**Dataset:** `seed/eval/golden_qa.jsonl` — 45 questions across destinations, visas,
policies, hotels, and FAQ docs, each with an `expected_source_doc` and
`reference_answer` derived directly from the real `seed/docs/` content.

**Method:** `evaluation/retrieval_eval.py::compute_metrics()` calls
`rag_service.retrieve_documents()` for each question and checks whether the
`expected_source_doc` filename appears in the top-`k` retrieved chunks'
`filename` metadata. Precision@k / Recall@k / MRR computed locally (no LLM,
no network dependency) so the CI gate (`tests/test_eval_retrieval.py`) never
depends on external connectivity.

**Real results (2026-08-04, full local Ollama + Chroma DB + mock API):**

| Metric | Value |
|---|---|
| n_examples | 45 |
| k | 4 |
| recall_at_k | 1.0 |
| precision_at_k | 0.25 |
| mrr | 0.989 |

`precision_at_k = 0.25` is expected, not a defect: with exactly one relevant
document per question and `k=4`, perfect recall mathematically caps precision
at `1/k`. Recall@k and MRR are the meaningful quality signals here.

**CI gate thresholds** (`tests/test_eval_retrieval.py`): `recall_at_k >= 0.85`,
`mrr >= 0.8` — calibrated with margin below the observed perfect scores.

**Still pending:** re-run with one variable changed (chunk size or k) via a
throwaway Chroma directory, and add the before/after comparison here.

- [SCREENSHOT NEEDED: LangSmith Experiments table showing the retrieval-eval experiment run, once `run_langsmith_experiment()` is executed on a machine with LangSmith access]

---

## 3. Generation evaluation (LLM-as-judge)

**System under test:** `rag_service.get_policy_answer()` (`MODEL_NAME`, e.g. `llama3.1:8b`).
**Judge:** a *different* local Ollama model (`JUDGE_MODEL_NAME`, e.g.
`qwen2.5:7b`) so the judge isn't grading its own homework — no external API
or account needed, reproducible by any student with Ollama installed.

`evaluation/generation_eval.py::run_generation_eval()` sweeps all 45 golden
questions, grades each answer 1-5 for faithfulness/groundedness against
`reference_answer`, and reports the overall average plus a separate average
for the 12 visa-only questions.

`hallucinated_visa_case()` is an explicit adversarial check (not left to
chance): it feeds the judge a deliberately wrong France-visa answer ("365
days", "no passport needed") to prove the judge actually catches the domain's
flagship failure mode — a hallucinated visa answer that could strand a
traveler at the airport.

*Real results: pending a run on a machine with both `MODEL_NAME` and
`JUDGE_MODEL_NAME` pulled via Ollama.*

- [SCREENSHOT NEEDED: not applicable - this eval runs entirely locally, no LangSmith UI involved unless traced separately]

---

## 4. End-to-end scenario evaluation

*Not started yet — Phase E.*

---

## 5. CI quality gate / regression demo

*Deferred — repo now has git + GitHub remote
(https://github.com/ozearkhan/course_project_main), can revisit on request.*
