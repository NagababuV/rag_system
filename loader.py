from pypdf import PdfReader
from typing import List
import os

def load_pdfs(pdf_dir: str) -> List[str]:
    texts = []

    if not os.path.exists(pdf_dir):
        raise FileNotFoundError("PDF directory not found")

    for file in os.listdir(pdf_dir):
        if not file.lower().endswith(".pdf"):
            continue

        try:
            reader = PdfReader(os.path.join(pdf_dir, file))
            pdf_text = ""

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    pdf_text += text + "\n"

            if pdf_text.strip():
                texts.append(pdf_text)

        except Exception as e:
            print(f"Skipping invalid PDF {file}: {e}")

    if not texts:
        raise ValueError("No valid PDF text found")

    return texts
