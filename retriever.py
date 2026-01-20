def retrieve_context(vectordb, query: str, k: int = 8) -> str:
    """
    Retrieve relevant document chunks using query expansion
    to improve recall for large policy documents.
    """

    expanded_queries = [
        query,
        f"{query} in policy document",
        f"definition of {query}",
        "insurance company name",
        "name of insurer",
        "policy issued by"
    ]

    docs = []
    for q in expanded_queries:
        docs.extend(vectordb.similarity_search(q, k=3))

    # Remove duplicate chunks
    unique_docs = {doc.page_content: doc for doc in docs}.values()

    if not unique_docs:
        return ""

    return "\n\n".join(doc.page_content for doc in unique_docs)
