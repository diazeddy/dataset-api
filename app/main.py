"""
This module initializes the FastAPI application and includes the necessary routers for authentication and dataset management.
"""

from fastapi import FastAPI
from app.routes.AuthRouter import auth_router
from app.routes.DatasetRouter import dataset_router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    :return: Configured FastAPI application instance.
    """
    # Initialize FastAPI application
    app = FastAPI()

    # Include the authentication router with a prefix
    app.include_router(auth_router, prefix="/auth")

    # Include the dataset router with a prefix
    app.include_router(dataset_router, prefix="/datasets")

    return app


# Create the FastAPI application instance
app = create_app()
