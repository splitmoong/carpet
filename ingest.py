import os
from PyPDF2 import PdfReader
import dotenv

from preprocess import CleanPdfs

def extract_text(pdf_path):
    pdf_path = os.path.expanduser(pdf_path)
    pdf_path = os.path.abspath(pdf_path)
    if not os.path.exists(pdf_path):             
        raise FileNotFoundError(f"File not found: {pdf_path}")

    reader = PdfReader(pdf_path)
    return "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

dotenv.load_dotenv()
path = os.getenv('FILE_PATH')
text = extract_text(path)
clean_text = CleanPdfs.clean_text(text)
print(text[:500])
