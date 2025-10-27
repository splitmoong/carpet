import os
import re
from PyPDF2 import PdfReader


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract raw text from a PDF file.
    Returns all text concatenated from all pages.
    """
    pdf_path = os.path.abspath(os.path.expanduser(pdf_path))
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"File not found: {pdf_path}")

    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def preprocess_pdf_text(raw_text: str) -> str:
    """
    Clean and normalize extracted PDF text.
    - Remove extra spaces and newlines
    - Remove page numbers or standalone digits
    - Normalize quotes and apostrophes
    Returns a single flattened string suitable for embeddings.
    """
    # Remove carriage returns and form feeds
    text = raw_text.replace("\r", " ").replace("\f", " ")

    # Collapse all whitespace (spaces, tabs, newlines) into one space
    text = re.sub(r'\s+', ' ', text, flags=re.UNICODE)

    # Remove standalone digits (page numbers, isolated numbers)
    text = re.sub(r'\b\d+\b', '', text)

    # Normalize punctuation
    text = text.replace("“", '"').replace("”", '"').replace("’", "'")

    return text.strip()


def extract_and_preprocess(pdf_path: str) -> str:
    """
    Convenience function to extract and preprocess PDF text in one step.
    """
    raw_text = extract_text_from_pdf(pdf_path)
    return preprocess_pdf_text(raw_text)
