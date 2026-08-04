import os

from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings


load_dotenv()


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


db = Chroma(
    persist_directory=os.getenv("CHROMA_DB"),
    embedding_function=embeddings,
)


def test_rag_search():

    docs = db.similarity_search(
        "visa",
        k=2,
    )

    assert len(docs) > 0