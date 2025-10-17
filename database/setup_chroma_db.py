import os
from chromadb import PersistentClient

def setup_chroma(path: str):
    if not os.path.exists(path):
        os.makedirs(path)
    client = PersistentClient(path=path)
    client.get_or_create_collection("user_files")
    print(f"ChromaDB initialized at: {os.path.abspath(path)}")
    return client
