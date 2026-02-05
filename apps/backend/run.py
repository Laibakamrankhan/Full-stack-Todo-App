#!/usr/bin/env python3
"""
Entry point for Hugging Face Spaces deployment
"""

import os
import sys
import logging

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from app import app
import uvicorn

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Get port from environment or default to 8000
    port = int(os.environ.get("PORT", 8000))

    print(f"Starting Todo API server on port {port}")

    # Run the application with uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main()