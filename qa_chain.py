from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, LLM_MODEL

llm = ChatOpenAI(
    model=LLM_MODEL,
    temperature=0,
    openai_api_key=OPENAI_API_KEY
)

def generate_answer(context: str, query: str) -> str:
    if not context.strip():
        return "Answer not found in provided documents"

    prompt = f"""
You are an AI assistant.
Answer ONLY using the context below.
If the answer is not explicitly present, say:
"Answer not found in provided documents"

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)
    return response.content.strip()
