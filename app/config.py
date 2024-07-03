"""
This module defines the application settings using Pydantic for environment variable management.
"""

import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from a .env file
load_dotenv()


class AppConfig(BaseSettings):
    """
    Defines configuration settings for the application.

    Attributes:
        DATABASE_URL (str): The URL for the database connection.
        DATABASE_NAME (str): The name of the database.
        SECRET_KEY (str): The secret key used for JWT encoding and decoding.
        ALGORITHM (str): The algorithm used for JWT token creation.
        ACCESS_TOKEN_EXPIRE_SECONDS (int): The expiration time for access tokens in seconds.
    """
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 1800


# Instantiate the settings object to be used throughout the application
app_config = AppConfig()
