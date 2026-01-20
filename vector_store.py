from langchain_community.vectorstores import Chroma
from embeddings import get_embedding_model
from typing import List
import os

def create_or_load_vector_db(chunks: List[str], persist_dir: str):
    embedding_model = get_embedding_model()

    # Load existing DB if present
    if os.path.exists(persist_dir) and os.listdir(persist_dir):
        return Chroma(
            persist_directory=persist_dir,
            embedding_function=embedding_model
        )

    # Otherwise create new DB
    vectordb = Chroma.from_texts(
        texts=chunks,
        embedding=embedding_model,
        persist_directory=persist_dir
    )

    vectordb.persist()
    return vectordb
