#!/usr/bin/env python3
import sys
import os
from dotenv import load_dotenv

from database.setup_chroma_db import setup_chroma
from ingestion.ingestor import Ingestor
from ollama.ollama import Ollama

# init or connect to Chroma
from chromadb import PersistentClient

# from search_db import search_vector_db

load_dotenv()

import logging

# Suppress a noisy Chroma telemetry INFO message coming from the
# chromadb.telemetry.product.posthog logger. The library still runs
# telemetry, but this prevents the startup INFO line from printing.
logging.getLogger("chromadb.telemetry.product.posthog").setLevel(logging.WARNING)

# GLOBAL DB in home directory
HOME = os.path.expanduser("~")
db_path = os.path.join(HOME, "chroma_store")

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

    if command == "ollama":
        Ollama.start()
        return
    
    if command == "model":
        Ollama.check_model()
        return

    if command == "embed":

        #check for ollama installation
        if not Ollama.start_from_embed():
            Ollama.start()

        cwd = os.getcwd()
        ingestor = Ingestor()
        ingestor.open_folder(cwd)
        print(f"Found {len(ingestor.file_paths)} files to embed.")
        return

    if command == "search":
        if len(sys.argv) < 3:
            print("Usage: carpet search <query>")
            return
        query = " ".join(sys.argv[2:])
        # results = search_vector_db(query, collection)
        print(f"Searching for: {query}")
        return

    print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
