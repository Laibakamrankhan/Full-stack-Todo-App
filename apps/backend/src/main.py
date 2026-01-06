from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth_router, tasks_router
from .core.middleware import AuthMiddleware
from .core.config import settings
from .core.logging_config import setup_logging
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
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )