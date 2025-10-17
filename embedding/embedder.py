from os import path
from chromadb import PersistentClient
from typing import Callable


class Embedder:

    def __init__(self):
        self.handlers: dict[str, Callable[[str], None]] = {
            ".pdf": self._embed_pdf,
        }

    def _embed_pdf(self, file_path : str):
        from sentence_transformers import SentenceTransformer
        from extract.pdf.extract_preprocess_pdf import extract_and_preprocess
        txt = extract_and_preprocess(file_path)
        print(txt)
        pass

    def embed(self, file_path : str):
        ext = path.splitext(file_path)[1].lower()

        if ext in self.handlers:
            self.handlers[ext](file_path)
        else:
            print(f"Skipping unsupported file type: {file_path}")
        pass


    pass