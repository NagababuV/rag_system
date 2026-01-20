import streamlit as st
import os

from app import ask_question
from loader import load_pdfs
from splitter import split_text
from vector_store import create_or_load_vector_db
from qa_chain import generate_document_questions
from config import VECTOR_DB_DIRECTORY

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Document Assistant",
    page_icon="📄",
    layout="centered"
)

# ---------------- HEADER ----------------
st.title("📄 Document Assistant")

st.markdown(
    """
    Upload large documents such as **company policies or insurance policies**
    (even 50–100+ pages) and ask questions to get accurate answers instantly.

    Answers are provided **strictly from the uploaded documents**.
    """
)

# ---------------- PDF UPLOAD ----------------
st.markdown("---")
st.subheader("📂 Upload Documents")

uploaded_files = st.file_uploader(
    "Upload one or more PDF files",
    type=["pdf"],
    accept_multiple_files=True
)

documents_ready = False
suggested_questions = []

if uploaded_files:
    os.makedirs("data/pdfs", exist_ok=True)

    for file in uploaded_files:
        with open(f"data/pdfs/{file.name}", "wb") as f:
            f.write(file.read())

    st.success("✅ Documents uploaded successfully")

    with st.spinner("Processing documents..."):
        texts = load_pdfs("data/pdfs")
        chunks = split_text(texts)
        vector_db = create_or_load_vector_db(chunks, VECTOR_DB_DIRECTORY)

        combined_text = "\n\n".join(texts)
        suggested_questions = generate_document_questions(combined_text)

    documents_ready = True
    st.success("📘 Documents are ready for questions")

# ---------------- DYNAMIC QUESTIONS ----------------
if documents_ready and suggested_questions:
    st.markdown("---")
    st.subheader("💡 Suggested Questions From Your Document")

    st.info(
        "These questions are automatically generated from the uploaded document. "
        "You can copy any question and paste it below."
    )

    for q in suggested_questions:
        st.code(q, language="text")

# ---------------- ASK QUESTION ----------------
st.markdown("---")
st.subheader("🔍 Ask a Question")

query = st.text_input(
    "Enter your question",
    placeholder="Paste a suggested question or type your own..."
)

if st.button("Ask"):
    if not query.strip():
        st.warning("Please enter a valid question.")
    else:
        with st.spinner("Searching documents..."):
            answer = ask_question(query)

        st.subheader("📌 Answer")
        st.write(answer)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "This assistant provides answers strictly based on the uploaded documents."
)
