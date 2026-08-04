import os
import shutil
from datetime import datetime

from dotenv import load_dotenv

from langchain_community.document_loaders import (
    DirectoryLoader,
    TextLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# ==========================================================
# Load Environment Variables
# ==========================================================

load_dotenv()

DOCUMENT_PATH = os.getenv("DOCUMENT_PATH")
CHROMA_DB = os.getenv("CHROMA_DB")

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ==========================================================
# Configuration
# ==========================================================

DESTINATIONS = [
    "paris",
    "tokyo",
    "kyoto",
    "osaka",
    "bali",
    "singapore",
    "lisbon",
    "dubai",
    "london",
    "rome",
]

SENSITIVE_DOCUMENTS = {
    "internal_customer_records.md",
    "commission_table.md",
}

# ==========================================================
# Metadata
# ==========================================================

def add_metadata(documents):

    for doc in documents:

        source = doc.metadata["source"]

        filename = os.path.basename(source)
        filename_lower = filename.lower()

        folder = os.path.basename(os.path.dirname(source)).lower()

        # --------------------------------------------------
        # Required Metadata
        # --------------------------------------------------

        doc.metadata["filename"] = filename

        doc.metadata["source_path"] = source

        doc.metadata["last_updated"] = datetime.fromtimestamp(
            os.path.getmtime(source)
        ).strftime("%Y-%m-%d")

        # --------------------------------------------------
        # Document Type
        # --------------------------------------------------

        if folder == "destinations":
            doc.metadata["doc_type"] = "destination"

        elif folder == "visas":
            doc.metadata["doc_type"] = "visa"

        elif folder == "policies":
            doc.metadata["doc_type"] = "policy"

        elif folder == "hotels":
            doc.metadata["doc_type"] = "hotel"

        else:
            doc.metadata["doc_type"] = "general"

        # --------------------------------------------------
        # Destination
        # --------------------------------------------------

        destination = "General"

        for city in DESTINATIONS:

            if city in filename_lower:
                destination = city.title()
                break

        doc.metadata["destination"] = destination

    return documents

# ==========================================================
# Load Documents
# ==========================================================

def load_documents():

    loader = DirectoryLoader(
        DOCUMENT_PATH,
        glob="**/*.md",
        loader_cls=TextLoader,
    )

    documents = loader.load()

    filtered_documents = []
    skipped_documents = []

    for doc in documents:

        filename = os.path.basename(doc.metadata["source"])

        if filename.lower() in SENSITIVE_DOCUMENTS:
            skipped_documents.append(filename)
            continue

        filtered_documents.append(doc)

    filtered_documents = add_metadata(filtered_documents)

    print(f"\nLoaded Documents : {len(filtered_documents)}")

    if skipped_documents:

        print(f"Skipped Sensitive Documents : {len(skipped_documents)}")

        for file in skipped_documents:
            print(f"   • {file}")

    return filtered_documents

# ==========================================================
# Split Documents
# ==========================================================

def split_documents(documents):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100,
    )

    chunks = splitter.split_documents(documents)

    print(f"\nCreated Chunks : {len(chunks)}")

    if chunks:

        print("\nSample Metadata")
        print("-" * 40)

        for key, value in chunks[0].metadata.items():
            print(f"{key}: {value}")

        print("-" * 40)

    return chunks

# ==========================================================
# Create Vector Database
# ==========================================================

def create_vector_database(chunks):

    embeddings = HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL
    )

    if os.path.exists(CHROMA_DB):

        shutil.rmtree(CHROMA_DB)

        print("\nOld Chroma database removed.")

    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DB,
    )

    print("New Chroma database created successfully.")

# ==========================================================
# Main
# ==========================================================

def main():

    print("=" * 60)
    print("TripPilot Knowledge Base Ingestion")
    print("=" * 60)

    documents = load_documents()

    chunks = split_documents(documents)

    create_vector_database(chunks)

    print("\nIngestion completed successfully.")
    print(f"Database Location : {CHROMA_DB}")
    print("=" * 60)

# ==========================================================
# Entry Point
# ==========================================================

if __name__ == "__main__":
    main()