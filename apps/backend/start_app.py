#!/usr/bin/env python3
"""
Standalone startup script for the FastAPI application on Railway
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def install_dependencies():
    """Install required dependencies if not already installed"""
    print("Installing dependencies...")

    # Install from requirements.txt
    result = subprocess.run([
        sys.executable, "-m", "pip", "install",
        "--root-user-action=ignore",
        "-r", "requirements.txt"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error installing requirements: {result.stderr}")
        return False

    # Ensure uvicorn is installed
    result = subprocess.run([
        sys.executable, "-m", "pip", "install",
        "--root-user-action=ignore",
        "uvicorn[standard]"
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error installing uvicorn: {result.stderr}")
        return False

    print("Dependencies installed successfully")
    return True

def main():
    # Change to the directory where this script is located
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    print(f"Changed to directory: {script_dir}")

    # Install dependencies
    if not install_dependencies():
        print("Failed to install dependencies")
        sys.exit(1)

    # Now try to import and run the application
    try:
        # Add current directory to Python path
        sys.path.insert(0, str(script_dir))

        # Import uvicorn and the app
        import uvicorn

        # Import the app from main.py
        main_spec = importlib.util.spec_from_file_location("main", script_dir / "main.py")
        main_module = importlib.util.module_from_spec(main_spec)
        main_spec.loader.exec_module(main_module)

        # Get the app instance
        app = main_module.app

        # Get port from environment
        port = int(os.environ.get("PORT", 8000))

        print(f"Starting server on port {port}")
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")

    except ImportError as e:
        print(f"Import error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"Error running application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()