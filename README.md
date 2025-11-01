# Carpet 

Carpet is a small CLI toolkit to embed, and search documents locally, integrating the Ollama local LLM manager.

## Features
- Embed files from a folder (all files reachable).
- Search for a file with a query, returns top 4 results.
- Manage a local Chroma vector store, see and delete the embeddings.
- Integrate with Ollama to detect, pull, and use local model (e.g. `qllama/bge-m3`)

<img width="2109" height="956" alt="Group 1(1)" src="https://github.com/user-attachments/assets/c481204d-f7fa-437a-a9bc-335977982d18" />
<img width="2109" height="831" alt="Screenshot From 2025-11-01 12-56-47 1" src="https://github.com/user-attachments/assets/b4a840cd-9947-4e57-99bb-bf91beb0ee83" />
<img width="2111" height="833" alt="Screenshot From 2025-11-01 13-02-53 1" src="https://github.com/user-attachments/assets/100c7ae0-5c02-4f51-a16e-a26ac3aa51d6" />
<img width="2111" height="596" alt="Group 2(1)" src="https://github.com/user-attachments/assets/354b7d09-b2e2-4718-b639-6f7801a10d50" />

## Installation

Linux / MacOS

```bash
chmod +x script.sh
./script.sh
```

Windows 

You can create a symlink with `mklink` in an elevated prompt or with Developer Mode enabled:

```powershell
# Run in an Administrator CMD prompt
mklink "C:\Users\YourName\bin\carpet.py" "C:\full\path\to\repo\main.py"
```

(will add a script.bat in future which will work same as script.sh)

## Usage

```bash
carpet <command>
```

Commands
- `ollama` — Check for a local `ollama` CLI installation and optionally install it. This will:
	- detect whether `ollama` is present on PATH
	- on Linux/macOS, offer to run the official installer script
	- on native Windows, print safe manual install instructions

- `model` — Check if the "qllama/bge-m3" model exists in the user's system, pull if it doesn't.

- `embed` — Walk the current working directory, ingest files and prepare embeddings. The command will print how many files were found to embed.

- `search "query"` — Run a vector search against the local Chroma collection and return top 4 similar files.

- `db` — See all the filepaths and their chunks in ChromaDb.

- `delete "filepath"` — Delete the embedding of a file from ChromaDb.

