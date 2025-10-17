from sentence_transformers import SentenceTransformer
import numpy as np

from chromadb import PersistentClient

class Embedder:

    def embed():
        model = SentenceTransformer("all-MiniLM-L6-v2")
        # embeddings = model.encode(chunks)