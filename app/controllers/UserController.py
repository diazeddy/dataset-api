"""
This module provides helper functions for interacting with the user collection in the database.
"""


def get_user_by_email(collection, email: str) -> dict:
    """
    Retrieve a user document by email.

    :param collection: The mongo db collection.
    :param email: The email of the user to retrieve.
    :return: A dictionary containing the user document or None if not found.
    """
    user = collection.find_one(filter={"email": email})
    return user


def is_user_exist(collection, email: str) -> bool:
    """
    Check if a user exists in the database by email.

    :param collection: The mongo db collection.
    :param email: The email of the user to check.
    :return: True if the user exists, False otherwise.
    """
    user = get_user_by_email(collection, email)
    return user is not None


def insert_new_user(collection, email: str, password: str) -> None:
    """
    Insert a new user document into the collection.

    :param collection: The mongo db collection.
    :param email: The email of the new user.
    :param password: The hashed password of the new user.
    """
    collection.insert_one({
        "email": email,
        "password": password
    })
