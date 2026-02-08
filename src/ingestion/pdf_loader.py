from PyPDF2 import PdfReader
import os


def load_policy_pdf(filepath):
    """
    Extract text from a PDF policy document (offline).
    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"PDF file not found: {filepath}")

    reader = PdfReader(filepath)
    extracted_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            extracted_text.append(text)

    return "\n".join(extracted_text)
