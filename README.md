# Carpet 

Carpet is a small CLI toolkit to ingest, embed, and search documents locally, with optional integration for the Ollama local LLM manager. It's designed to be simple, flexible, and easy to extend.

## Features
- Ingest files from a folder and prepare them for embedding
- Create and manage a local Chroma vector store
- Integrate with Ollama to detect, pull, and use local models (e.g. `qllama/bge-m3`)

<img alt="Screenshot From 2025-10-27 20-29-47 1" src="https://github.com/user-attachments/assets/d0697754-bc43-45f6-9b37-81585a4f64e2" style="width:100%; height:auto; display:block;" />
<img alt="Screenshot From 2025-10-27 21-29-10 1" src="https://github.com/user-attachments/assets/01757f3e-e18b-4d3a-83d2-5912c58be738" style="width:100%; height:auto; display:block;" />

## Installation

1. Create a virtual environment (recommended):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies (if a `requirements.txt` exists):

```bash
pip install -r requirements.txt
```

If you don't have a `requirements.txt`, the project requires the usual packages used here such as `chromadb` — check the `requirements.txt` from your collaborator or add the dependencies you need.

3. Create a Syslink

If you want to call the project as a single command (`carpet`) from any folder, create a small symlink or wrapper in a directory on your PATH. Below are safe, copy-pasteable options for Linux/macOS and Windows.

Linux / MacOS

```bash
# from the project root
chmod +x main.py
sudo ln -s /full/path/to/your/repo/main.py /usr/local/bin/carpet
```

Windows 

You can create a symlink with `mklink` in an elevated prompt or with Developer Mode enabled:

```powershell
# Run in an Administrator CMD prompt
mklink "C:\Users\YourName\bin\carpet.py" "C:\full\path\to\repo\main.py"
```

This approach is less portable and often unnecessary — the wrapper `.bat` is simpler and works reliably.

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

- `search <query>` — (Planned) run a vector search against the local Chroma collection.