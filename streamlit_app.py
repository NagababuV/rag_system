import streamlit as st
import os

from app import ask_question
from loader import load_pdfs
from splitter import split_text
from vector_store import create_or_load_vector_db
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
    ### Welcome 👋  
    This tool helps you **find accurate answers from your documents**.

    **What you can do:**
    - Upload one or more PDF documents
    - Ask questions related to those documents
    - Get answers strictly based on the uploaded content

    **Ideal for large documents (50–100+ pages):**
    - Company or HR policies
    - Insurance policy documents
    - Legal or compliance documents

    ⚠️ If an answer is not found in the documents, the assistant will clearly say so.
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

if uploaded_files:
    os.makedirs("data/pdfs", exist_ok=True)

    for file in uploaded_files:
        with open(f"data/pdfs/{file.name}", "wb") as f:
            f.write(file.read())

    st.success("✅ Documents uploaded successfully")

    with st.spinner("Processing documents, please wait..."):
        texts = load_pdfs("data/pdfs")
        chunks = split_text(texts)
        vector_db = create_or_load_vector_db(chunks, VECTOR_DB_DIRECTORY)

    documents_ready = True
    st.success("📘 Documents are ready for questions")

# ---------------- SUGGESTED QUESTIONS ----------------
if documents_ready:
    st.markdown("---")
    st.subheader("💡 Suggested Questions Based on Your Documents")

    st.markdown(
        """
        Below are some **important questions commonly found in policy and insurance documents**.  
        You can **copy any question and paste it into the Ask box**.
        """
    )

    suggested_questions = [
        "What is the refund or cancellation policy?",
        "How many sick leaves are allowed per year?",
        "Is remote work permitted?",
        "What is the notice period for termination?",
        "What benefits are provided to employees?",
        "What does the insurance policy cover?",
        "Is there any waiting period mentioned in the policy?",
        "Are there any exclusions mentioned in the document?",
        "How long does it take to process a refund or claim?",
        "What are the key terms and conditions?"
    ]

    for q in suggested_questions:
        st.code(q, language="text")  # built-in copy button

# ---------------- ASK QUESTION ----------------
st.markdown("---")
st.subheader("🔍 Ask a Question")

query = st.text_input(
    "Enter your question",
    placeholder="Paste a suggested question or type your own..."
)

if st.button("Ask"):
    if not query.strip():
        st.warning("⚠️ Please enter a valid question.")
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
