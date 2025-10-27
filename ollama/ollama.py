"""Utilities for detecting and installing the `ollama` CLI.

This module provides a simple `Ollama` class with a `check` method that
verifies whether the `ollama` executable is present on PATH. If it is not
found the module can run the official installer script to download and
install `ollama` on Linux/macOS systems.

Notes:
- For safety the installer will be run only after explicit user confirmation
  when invoked from the command line. Callers can programmatically disable
  the prompt by calling `install_ollama(prompt=False)`.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import logging
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Ollama:
    """Helper class for checking and (optionally) installing ollama."""

    @staticmethod
    def check() -> bool:
        """Return True if the `ollama` executable is available on PATH.
        Also logs a short message indicating status.
        """
        bin_path = shutil.which("ollama")
        if bin_path:
            try:
                result = subprocess.run(
                    [bin_path, "version"], capture_output=True, text=True, check=False
                )
                ver = result.stdout.strip() or result.stderr.strip()
                logger.info("Found ollama at %s. Version/info: %s", bin_path, ver)
            except Exception as exc:  # pragma: no cover - defensive logging
                logger.info("Found ollama at %s (could not run version): %s", bin_path, exc)
            return True

        logger.info("`ollama` executable not found on PATH.")
        return False

    @staticmethod
    def install_ollama(prompt: bool = True) -> Optional[int]:
        """Attempt to download and run the official ollama installer.

        If prompt is True the user will be asked to confirm before the
        installer is executed. Returns the subprocess return code on execution,
        or None if the install was skipped.
        """
        # If running on native Windows, don't attempt to run the POSIX shell installer;
        # instead provide instructions to the user and exit.
        if sys.platform == "win32":
            msg = (
                "Automatic installation is not supported on native Windows by this script.\n"
                "Please install ollama manually. Options:\n"
                " - Use Git Bash/MSYS2 if you have curl: curl -sSf https://ollama.ai/install.sh | sh\n"
                " - Use a native Windows package manager (winget/choco) or download the installer from https://ollama.ai\n"
                "After installation, restart your terminal and re-run this command."
            )
            logger.info(msg)
            print(msg)
            return None

        if prompt:
            try:
                resp = input("`ollama` not found. Download and install ollama now? [y/N]: ")
            except EOFError:
                # non-interactive environment
                resp = "n"

            if resp.strip().lower() not in ("y", "yes"):
                logger.info("Installation cancelled by user.")
                return None

        # Try curl first, fall back to wget if curl is not available.
        curl = shutil.which("curl")
        wget = shutil.which("wget")

        if curl:
            cmd = "/bin/sh -c \"curl -sSf https://ollama.ai/install.sh | sh\""
        elif wget:
            # wget -qO- URL | sh
            cmd = "/bin/sh -c \"wget -qO- https://ollama.ai/install.sh | sh\""
        else:
            logger.error("Neither curl nor wget found; cannot download installer automatically.")
            return None

        logger.info("Running installer command: %s", cmd)
        # Use shell to run the pipeline; keep it simple and capture output.
        try:
            proc = subprocess.run(cmd, shell=True)
            if proc.returncode == 0:
                logger.info("Installer finished. Please re-run `ollama` checks if needed.")
            else:
                logger.error("Installer exited with return code %s", proc.returncode)
            return proc.returncode
        except Exception as exc:  # pragma: no cover - runtime failures
            logger.exception("Failed to run installer command: %s", exc)
            return None

    @staticmethod
    def start() -> bool:
        """Domino starter: check for ollama and attempt installation if missing.

        Returns True if ollama is present or installation completed successfully,
        False otherwise.
        """
        present = Ollama.check()
        if present:
            print("ollama is already installed on this system.")
            return True

        code = Ollama.install_ollama(prompt=True)
        if code is None:
            print("ollama was not installed.")
            return False
        elif code == 0:
            print("Installation completed (exit code 0). You may need to restart your shell.")
            return True
        else:
            print(f"Installation failed with exit code {code}.")
            return False
        
    def start_from_embed() -> bool:
        present = Ollama.check()
        if not present:
            return False
        else:
            return True
