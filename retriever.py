def retrieve_context(vectordb, query: str, k: int = 4) -> str:
    docs = vectordb.similarity_search(query, k=k)

    if not docs:
        return ""

    return "\n\n".join(doc.page_content for doc in docs)
