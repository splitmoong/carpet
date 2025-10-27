import os
from chromadb import PersistentClient


def setup_chroma(path: str):
    """Create persistent ChromaDB at `path` if it doesn't exist, and return client + collection."""
    if not os.path.exists(path):
        os.makedirs(path)

    client = PersistentClient(path=path)
    collection = client.get_or_create_collection("user_files")
    print(f"ChromaDB initialized at: {os.path.abspath(path)}")
    return client, collection
