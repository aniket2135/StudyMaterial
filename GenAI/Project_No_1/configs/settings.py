import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]

PDF_DIRECTORY = BASE_DIR / os.getenv("PDF_PATH")

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-small-en-v1.5"
)

CHROMA_PATH = BASE_DIR / os.getenv(
    "CHROMA_PATH",
    "vectorstore/chroma"
)

CHROMA_COLLECTION = os.getenv(
    "CHROMA_COLLECTION",
    "documents"
)

print(PDF_DIRECTORY)