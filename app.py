from loader import load_pdfs
from splitter import split_text
from vector_store import create_or_load_vector_db
from retriever import retrieve_context
from qa_chain import generate_answer
from config import PDF_DIRECTORY, VECTOR_DB_DIRECTORY

# Load and prepare vector DB at startup
try:
    texts = load_pdfs(PDF_DIRECTORY)
    chunks = split_text(texts)
    vector_db = create_or_load_vector_db(chunks, VECTOR_DB_DIRECTORY)
except Exception as e:
    raise RuntimeError(f"Failed to initialize RAG system: {e}")


def ask_question(query: str) -> str:
    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    context = retrieve_context(vector_db, query)
    return generate_answer(context, query)


# Example CLI usage
if __name__ == "__main__":
    while True:
        user_query = input("\nAsk a question (or type 'exit'): ")
        if user_query.lower() == "exit":
            break

        try:
            print("\nAnswer:\n", ask_question(user_query))
        except Exception as err:
            print("Error:", err)
