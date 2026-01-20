import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise EnvironmentError("OPENAI_API_KEY not found")

PDF_DIRECTORY = "data/pdfs"
VECTOR_DB_DIRECTORY = "data/vector_db"

# Optimized for large policy documents
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 400

EMBEDDING_MODEL = "text-embedding-3-small"
LLM_MODEL = "gpt-4o-mini"
