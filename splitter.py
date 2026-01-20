from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from config import CHUNK_SIZE, CHUNK_OVERLAP

def split_text(texts: List[str]) -> List[str]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = []
    for text in texts:
        chunks.extend(splitter.split_text(text))

    if not chunks:
        raise ValueError("Text splitting produced no chunks")

    return chunks
