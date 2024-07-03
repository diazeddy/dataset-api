"""
This module establishes a connection to a MongoDB database and retrieves the collections.
"""

from pymongo import MongoClient
from app.config import app_config


def get_database():
    """
    Connects to the MongoDB database using the provided settings and retrieves the collections.

    Returns:
        tuple: A tuple containing the user collection and dataset collection.
    """
    # Create a MongoDB client using the database URL from settings
    mongo_client = MongoClient(app_config.DATABASE_URL)

    # Access the specified database using the database name from settings
    database = mongo_client[app_config.DATABASE_NAME]

    return database
