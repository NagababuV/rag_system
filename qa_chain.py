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
Answer the question strictly using the context below.
If the answer is not present, say:
"Answer not found in provided documents"

Context:
{context}

Question:
{query}
"""

    response = llm.invoke(prompt)
    return response.content.strip()


def generate_document_questions(document_text: str) -> list[str]:
    """
    Generate document-specific important questions dynamically.
    """

    prompt = f"""
You are helping users understand a long policy or insurance document.

Based ONLY on the content below, generate 8–10 important questions
that users are likely to ask.

Rules:
- Questions must be answerable from the document
- Focus on insurer, policy type, benefits, exclusions, terms
- Do NOT invent information
- Return only a numbered list of questions

Document content:
{document_text[:6000]}
"""

    response = llm.invoke(prompt)

    questions = []
    for line in response.content.split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            questions.append(line.split(".", 1)[-1].strip())

    return questions
