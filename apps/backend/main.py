from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import everything directly by specifying the full path
import sys
import os
import importlib.util

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Now import the required modules directly
from src.api import auth_router, tasks_router
from src.core.middleware import AuthMiddleware
from src.core.config import settings
from src.core.logging_config import setup_logging
import uvicorn
import logging


def create_app():
    # Set up logging when the application starts
    setup_logging()
    logging.info("Application starting up")

    app = FastAPI(
        title="Todo API",
        description="A secure, full-stack todo application with authentication",
        version="0.1.0"
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify your frontend domain
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add authentication middleware
    app.add_middleware(AuthMiddleware)

    # Include API routes
    app.include_router(auth_router)
    app.include_router(tasks_router)

    @app.get("/")
    def read_root():
        return {"message": "Welcome to the Todo API"}

    return app


app = create_app()


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)