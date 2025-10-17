#!/usr/bin/env python3
import sys
import os
from dotenv import load_dotenv

from database.setup_chroma_db import setup_chroma
from ingestion.ingestor import Ingestor
# from search_db import search_vector_db

load_dotenv()

# GLOBAL DB in home directory
HOME = os.path.expanduser("~")
db_path = os.path.join(HOME, "chroma_store")

# init or connect to Chroma
from chromadb import PersistentClient
if not os.path.exists(db_path) or not os.listdir(db_path):
    client = setup_chroma(db_path)
else:
    client = PersistentClient(path=db_path)

collection = client.get_or_create_collection("user_files")


def main():
    if len(sys.argv) < 2:
        print("Usage: carpet <command> [args]")
        return

    command = sys.argv[1].lower()

    if command == "embed":
        cwd = os.getcwd()
        ingestor = Ingestor()
        ingestor.open_folder(cwd)
        print(f"Found {len(ingestor.file_paths)} files to embed.")

    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: carpet search <query>")
            return
        query = " ".join(sys.argv[2:])
        # results = search_vector_db(query, collection)
        print(f"Searching for: {query}")

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
