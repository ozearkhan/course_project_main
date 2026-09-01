import json
import os
from concurrent.futures import ThreadPoolExecutor

from langchain_ollama import ChatOllama
from pydantic import BaseModel, Field

from rag_service import get_policy_answer

GOLDEN_QA_PATH = os.path.join("seed", "eval", "golden_qa.jsonl")
JUDGE_CALIBRATION_PATH = os.path.join("seed", "eval", "judge_calibration.jsonl")
ANSWER_CACHE_PATH = os.path.join("evaluation", ".cache", "generation_answer_cache.json")

# Deliberately a DIFFERENT model than MODEL_NAME (the app's answer-generation
# model) so the judge isn't grading its own homework. Any locally pulled
# Ollama model works - default assumes `ollama pull qwen2.5:7b`.
MODEL_NAME = os.getenv("MODEL_NAME")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
JUDGE_MODEL_NAME = os.getenv("JUDGE_MODEL_NAME", "qwen2.5:7b")

# Bounded concurrency for judge calls - the judge model may not benefit from
# high concurrency unless Ollama is configured with OLLAMA_NUM_PARALLEL > 1,
# but this is still a no-cost lever to try.
MAX_JUDGE_WORKERS = int(os.getenv("MAX_JUDGE_WORKERS", "4"))

# Call counters for Part 1 timing/instrumentation - reset per process, read
# via get_call_counts(). Only real (non-cached) calls are counted.
_call_counts = {"generation_calls": 0, "judge_calls": 0}


def get_call_counts():
    return dict(_call_counts)


JUDGE_INSTRUCTIONS = """You are grading whether a travel assistant's answer is faithful and \
grounded in the reference answer for a question about travel policies, visas, \
destinations, or hotels.

Score 5: fully consistent with the reference, no fabricated facts.
Score 3: partially consistent, minor inaccuracies or omissions.
Score 1: contradicts the reference or invents facts not supported by it (a hallucination).

Be especially strict on visa/passport requirement questions - wrong validity \
periods, stay durations, or document requirements could strand a traveler at \
the airport."""


class FaithfulnessGrade(BaseModel):
    faithful: bool = Field(description="True if the answer has no hallucinated or contradicted facts relative to the reference")
    score: int = Field(description="Faithfulness/groundedness score from 1 (hallucinated/wrong) to 5 (fully faithful)")
    explanation: str = Field(description="Brief explanation of the score")


def load_golden_qa(path=GOLDEN_QA_PATH):

    examples = []

    with open(path, encoding="utf-8") as f:
        for line in f:
            examples.append(json.loads(line))

    return examples


def _load_answer_cache():

    if not os.path.exists(ANSWER_CACHE_PATH):
        return {}

    with open(ANSWER_CACHE_PATH, encoding="utf-8") as f:
        return json.load(f)


def _save_answer_cache(cache):

    os.makedirs(os.path.dirname(ANSWER_CACHE_PATH), exist_ok=True)

    with open(ANSWER_CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(cache, f, indent=2)


def get_cached_answer(question: str, cache: dict) -> str:
    """Reuses a previously generated answer unless MODEL_NAME changed (the
    cache key includes it), so re-running only re-judges, not re-generates."""

    key = f"{MODEL_NAME}::{question}"

    if key in cache:
        return cache[key]

    answer = get_policy_answer(question)
    _call_counts["generation_calls"] += 1
    cache[key] = answer

    return answer


def get_judge():
    return ChatOllama(
        model=JUDGE_MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        temperature=0,
    ).with_structured_output(FaithfulnessGrade)


def grade_answer(judge, question: str, reference_answer: str, actual_answer: str) -> dict:

    message = (
        f"Question: {question}\n"
        f"Reference Answer: {reference_answer}\n"
        f"Assistant's Answer: {actual_answer}"
    )

    grade = judge.invoke([
        {"role": "system", "content": JUDGE_INSTRUCTIONS},
        {"role": "user", "content": message},
    ])

    _call_counts["judge_calls"] += 1

    return grade.model_dump()


# ==========================================================
# Full sweep over the golden set (needs both Ollama models pulled)
# ==========================================================

def run_generation_eval(examples=None):

    examples = examples if examples is not None else load_golden_qa()

    judge = get_judge()
    cache = _load_answer_cache()

    # Generation is cached (serial - each answer needs its own retrieval +
    # LLM call anyway); judging is parallelized since it's the pure LLM-call
    # step and gains the most from concurrency.
    answers = [get_cached_answer(example["question"], cache) for example in examples]
    _save_answer_cache(cache)

    with ThreadPoolExecutor(max_workers=MAX_JUDGE_WORKERS) as pool:
        grades = list(pool.map(
            lambda pair: grade_answer(judge, pair[0]["question"], pair[0]["reference_answer"], pair[1]),
            zip(examples, answers),
        ))

    results = []

    for example, actual_answer, grade in zip(examples, answers, grades):
        results.append({
            "question": example["question"],
            "expected_source_doc": example["expected_source_doc"],
            "actual_answer": actual_answer,
            **grade,
        })

    scores = [r["score"] for r in results]
    visa_scores = [r["score"] for r in results if r["expected_source_doc"].endswith("_visa.md")]

    return {
        "n_examples": len(results),
        "avg_faithfulness_score": sum(scores) / len(scores) if scores else 0.0,
        "n_visa_examples": len(visa_scores),
        "avg_visa_faithfulness_score": sum(visa_scores) / len(visa_scores) if visa_scores else 0.0,
        "results": results,
    }


# ==========================================================
# Hallucinated-visa-requirements case (needs only the judge model pulled)
# Proves the judge actually catches the domain's flagship failure mode:
# a wrong visa answer that would strand a traveler at the airport.
# ==========================================================

def hallucinated_visa_case():

    return grade_answer(
        get_judge(),
        question="How long can I stay in France on a tourist Schengen visa?",
        reference_answer="Up to 90 days within any 180-day period.",
        actual_answer="You can stay in France for up to 365 days on a tourist Schengen visa, and no passport is required if you have a national ID card.",
    )


# ==========================================================
# Judge calibration (LLM-as-a-judge lesson 6.3): before trusting the judge,
# check it agrees with a small hand-labeled set of faithful/not-faithful pairs.
# ==========================================================

def load_calibration(path=JUDGE_CALIBRATION_PATH):

    examples = []

    with open(path, encoding="utf-8") as f:
        for line in f:
            examples.append(json.loads(line))

    return examples


def calibrate_judge(examples=None):

    examples = examples if examples is not None else load_calibration()
    judge = get_judge()

    with ThreadPoolExecutor(max_workers=MAX_JUDGE_WORKERS) as pool:
        grades = list(pool.map(
            lambda ex: grade_answer(judge, ex["question"], ex["reference_answer"], ex["candidate_answer"]),
            examples,
        ))

    agree = 0
    disagreements = []

    for ex, grade in zip(examples, grades):

        if grade["faithful"] == ex["human_faithful"]:
            agree += 1
        else:
            disagreements.append({
                "question": ex["question"],
                "human_faithful": ex["human_faithful"],
                "judge_faithful": grade["faithful"],
                "judge_explanation": grade["explanation"],
            })

    n = len(examples)

    return {
        "n": n,
        "agreement_rate": agree / n if n else 0.0,
        "disagreements": disagreements,
    }


if __name__ == "__main__":
    import sys

    demo = "--demo" in sys.argv

    if not demo:
        print("calibration:", {k: v for k, v in calibrate_judge().items() if k != "disagreements"})

    # --demo: same golden_qa.jsonl, just a 5-question stride slice - no
    # second file/function to keep in sync with the real 45.
    examples = load_golden_qa()[::9][:5] if demo else None
    summary = run_generation_eval(examples=examples)
    print({k: v for k, v in summary.items() if k != "results"})
    print("hallucinated_visa_case:", hallucinated_visa_case())
    print("call_counts:", get_call_counts())
