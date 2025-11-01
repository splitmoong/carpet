#!/bin/bash
set -e # exit immediately if a command exits with a non-zero status.

#source folder
SCRIPT_DIR="$( cd "$( dirname "$(readlink -f "$0")" )" &> /dev/null && pwd )"

VENV_PATH="${SCRIPT_DIR}/.venv"
VENV_PYTHON="${VENV_PATH}/bin/python"
MAIN_SCRIPT="${SCRIPT_DIR}/main.py"
LINK_NAME="carpet"
LINK_TARGET="/usr/local/bin/${LINK_NAME}"


#create venv
if [ ! -d "$VENV_PATH" ]; then
    echo "🐍 .venv not found. creating one in carpet's source folder..."
    
    (cd "$SCRIPT_DIR" && python3 -m venv .venv)
    
    echo "✅ venv created successfully."
    
    # Optionally, install necessary packages (e.g., packages needed by main.py)
    # UNCOMMENT the line below if you have a requirements.txt file
    # echo "📦 Installing required dependencies..."
    # "$VENV_PYTHON" -m pip install -r "${SCRIPT_DIR}/requirements.txt"
    # echo "✅ dependencies installed."
fi


#symlink
if [ ! -L "$LINK_TARGET" ] || [ "$(readlink -f "$LINK_TARGET")" != "$(readlink -f "$SCRIPT_DIR/script.sh")" ]; then
    echo "🔗 Creating global symlink '${LINK_NAME}' at ${LINK_TARGET} (requires sudo)..."
    # Remove old link if it exists and points elsewhere
    [ -L "$LINK_TARGET" ] && sudo rm "$LINK_TARGET"
    # Create the new symlink
    sudo ln -s "$SCRIPT_DIR/script.sh" "$LINK_TARGET"
    echo "✅ symlink created. call carpet by typing '${LINK_NAME}'"
fi


#execute
exec "$VENV_PYTHON" "$MAIN_SCRIPT" "$@"