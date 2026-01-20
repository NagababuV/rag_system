import streamlit as st
import os

# Import backend RAG functions
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

    **Ideal for large documents:**
    - Company policies
    - HR manuals
    - Insurance policy documents
    - Legal or compliance documents (50–100+ pages)

    Instead of manually searching through long PDFs, you can simply ask questions
    and get clear answers instantly.

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

    st.success("📘 Documents are ready for questions")

# ---------------- EXAMPLE QUESTIONS ----------------
st.markdown("---")
st.subheader("💡 Example Questions You Can Ask")

st.markdown(
    """
    Try asking questions like:

    - **What is the refund policy?**
    - **How many sick leaves are allowed per year?**
    - **Is remote work permitted?**
    - **What is the notice period for termination?**
    - **Which database is used in the system?**
    - **How long does refund processing take?**
    - **What does my insurance policy cover in case of hospitalization?**
    - **Is there any waiting period mentioned in the policy?**

    ❌ Questions unrelated to the uploaded documents will not be answered.
    """
)

# ---------------- ASK QUESTION ----------------
st.markdown("---")
st.subheader("🔍 Ask a Question")

query = st.text_input(
    "Enter your question",
    placeholder="Type your question here..."
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
