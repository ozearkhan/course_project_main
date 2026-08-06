import json
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from rag_service import get_policy_answer

GOLDEN_QA_PATH = os.path.join("seed", "eval", "golden_qa.jsonl")
JUDGE_MODEL = os.getenv("GEMINI_JUDGE_MODEL", "gemini-2.5-flash")

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


def get_judge():
    return ChatGoogleGenerativeAI(
        model=JUDGE_MODEL,
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

    return grade.model_dump()


# ==========================================================
# Full sweep over the golden set (needs Ollama + Gemini key)
# ==========================================================

def run_generation_eval(examples=None):

    examples = examples if examples is not None else load_golden_qa()
    judge = get_judge()

    results = []

    for example in examples:

        actual_answer = get_policy_answer(example["question"])

        grade = grade_answer(
            judge,
            example["question"],
            example["reference_answer"],
            actual_answer,
        )

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
# Hallucinated-visa-requirements case (needs only the Gemini key)
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


if __name__ == "__main__":
    summary = run_generation_eval()
    print({k: v for k, v in summary.items() if k != "results"})
    print("hallucinated_visa_case:", hallucinated_visa_case())
