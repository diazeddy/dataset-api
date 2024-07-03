"""
This module implements helper functions and classes for authentication and authorization using JWT and password hashing.
"""

from passlib.context import CryptContext
import time
import jwt

from app.config import app_config

# Initialize password context for hashing and verifying passwords
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify if the provided plain password matches the hashed password.

    :param plain_password: The plain text password to verify.
    :param hashed_password: The hashed password to compare against.
    :return: True if the password matches, False otherwise.
    """
    return password_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash the provided password.

    :param password: The plain text password to hash.
    :return: The hashed password.
    """
    return password_context.hash(password)


def generate_jwt(email: str) -> str:
    """
    Generate a JWT token for the given email.

    :param email: The email for which to generate the JWT token.
    :return: The generated JWT token.
    """
    payload = {
        "email": email,
        "expires": time.time() + app_config.ACCESS_TOKEN_EXPIRE_SECONDS  # Token expiration time
    }
    token = jwt.encode(payload, app_config.SECRET_KEY, algorithm=app_config.ALGORITHM)
    return token
