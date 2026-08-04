import os

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langsmith import traceable

from pii_filter import mask_pii

load_dotenv()

MODEL_NAME = os.getenv("MODEL_NAME")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL")
CHROMA_DB = os.getenv("CHROMA_DB")

TOP_K = 4

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = Chroma(
    persist_directory=CHROMA_DB,
    embedding_function=embeddings,
)

llm = ChatOllama(
    model=MODEL_NAME,
    base_url=OLLAMA_BASE_URL,
    temperature=0,
)

prompt = ChatPromptTemplate.from_template(
"""
You are TripPilot, a professional travel assistant.

Answer ONLY using the supplied context.

Rules:

1. Never use outside knowledge.
2. Combine information from multiple retrieved documents whenever appropriate.
3. If the answer is unavailable, reply exactly:

I couldn't find that information in the travel knowledge base.

4. Format the answer professionally using headings and bullet points whenever appropriate.

========================
Context
========================

{context}

========================
Question
========================

{question}
"""
)


@traceable(run_type="retriever")
def retrieve_documents(question: str):

    results = db.similarity_search_with_score(
        question,
        k=TOP_K,
    )

    return [doc for doc, score in results]


def get_policy_answer(question: str):

    docs = retrieve_documents(question)

    if not docs:
        return "I couldn't find that information in the travel knowledge base."

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    formatted_prompt = prompt.format(
        context=context,
        question=question,
    )

    response = llm.invoke(formatted_prompt)

    return mask_pii(response.content)