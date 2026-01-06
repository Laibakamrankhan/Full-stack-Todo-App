#!/usr/bin/env python3
"""
Start script for the FastAPI application on Railway
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    # Get the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)

    print(f"Changed to directory: {script_dir}")

    # Check if requirements.txt exists
    req_file = script_dir / "requirements.txt"
    if not req_file.exists():
        print(f"ERROR: requirements.txt not found at {req_file}")
        sys.exit(1)

    print("Installing dependencies from requirements.txt...")
    # Install dependencies
    result = subprocess.run([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ], cwd=script_dir)

    if result.returncode != 0:
        print("Failed to install dependencies")
        sys.exit(1)

    print("Dependencies installed successfully")

    # Now run the main application
    print("Starting the FastAPI application...")

    # Get the port from environment or default to 8000
    port = int(os.environ.get("PORT", 8000))

    # Import and run uvicorn
    try:
        import uvicorn
        from main import app

        print(f"Starting server on port {port}")
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=port,
            log_level="info"
        )
    except ImportError as e:
        print(f"Failed to import required modules: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()