import sys
import os

# Add the current directory and src directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from src.main import app

# This creates the FastAPI app instance that Hugging Face will look for
application = app  # For compatibility with different deployment platforms

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "src.main:app",  # Reference the app from src.main module
        host="0.0.0.0",
        port=port,
        reload=True
    )