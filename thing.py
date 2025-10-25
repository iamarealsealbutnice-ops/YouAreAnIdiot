#!/usr/bin/env python3
"""
run_bat.py

Downloads a .bat file from a GitHub raw URL and runs it locally.
WARNING: Only run this on files you trust. Inspect the downloaded .bat before execution.
"""

import os
import sys
import urllib.request
from pathlib import Path
import tempfile
import subprocess
import platform

# --------- CONFIGURE THIS ----------
# Replace this with the *raw* GitHub URL to your message.bat file.
# Example raw URL format:
# https://raw.githubusercontent.com/<username>/<repo>/main/message.bat
RAW_BAT_URL = "https://raw.githubusercontent.com/<iamarealsealbutnice-ops>/<YouAreAnIdiot>/main/bah.bat"

# Folder name inside Documents where the bat will be saved
DEST_FOLDER_NAME = "DownloadedBat"
# -----------------------------------

def is_windows():
    return platform.system().lower().startswith("windows")

def download_bat(url: str, dest_path: Path):
    print(f"Downloading from: {url}")
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
    except Exception as e:
        raise RuntimeError(f"Failed to download file: {e}")

    dest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(data)
    print(f"Saved .bat to: {dest_path}")

def inspect_file(dest_path: Path):
    print("\n--- START OF DOWNLOADED .bat (preview) ---")
    try:
        with open(dest_path, "r", encoding="utf-8", errors="replace") as f:
            for i, line in enumerate(f):
                # show first 50 lines max
                if i >= 50:
                    print("... (truncated) ...")
                    break
                print(line.rstrip("\n"))
    except Exception as e:
        print(f"Could not read file for preview: {e}")
    print("--- END OF PREVIEW ---\n")

def run_bat(dest_path: Path):
    print("Attempting to execute the batch file...")
    if is_windows():
        # Option 1: use os.startfile (opens in associated application)
        try:
            os.startfile(str(dest_path))
            print("Launched .bat using os.startfile (double-click behavior).")
            return
        except Exception:
            pass

        # Option 2: run via cmd /c start "" "path"
        try:
            subprocess.run(["cmd", "/c", "start", "", str(dest_path)], check=False)
            print("Launched .bat using cmd start.")
            return
        except Exception as e:
            print(f"Failed to launch .bat via cmd start: {e}")

        # Option 3: run directly (blocks)
        try:
            subprocess.run([str(dest_path)], shell=True, check=False)
            print("Executed .bat directly (may block until it finishes).")
            return
        except Exception as e:
            print(f"Failed to execute .bat directly: {e}")
            raise RuntimeError("Could not execute the batch file on this Windows system.")
    else:
        raise RuntimeError("This script is intended to run on Windows where .bat files are supported.")

def main():
    if RAW_BAT_URL.startswith("https://raw.githubusercontent.com/<"):
        print("Please set RAW_BAT_URL in the script to the raw GitHub URL of your message.bat file.")
        print("Example: https://raw.githubusercontent.com/your-username/your-repo/main/message.bat")
        sys.exit(1)

    if not is_windows():
        print("Warning: You're not on Windows. This script is meant to download and run a .bat on Windows.")
        # continue anyway to allow download, but execution will fail

    documents = Path.home() / "Documents"
    dest_folder = documents / DEST_FOLDER_NAME
    dest_bat = dest_folder / "message.bat"

    try:
        download_bat(RAW_BAT_URL, dest_bat)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    # Show file contents to user for inspection
    inspect_file(dest_bat)

    # Prompt user for confirmation before running
    response = input("Do you want to execute this .bat file now? (y/N): ").strip().lower()
    if response != "y":
        print("Aborting execution. You can inspect or run the file manually at:", dest_bat)
        sys.exit(0)

    try:
        run_bat(dest_bat)
    except Exception as e:
        print(f"Execution error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
