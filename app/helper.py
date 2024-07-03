"""
This module implements helper functions and classes for authentication and authorization using JWT and password hashing.
"""

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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


def decode_jwt(token: str) -> dict:
    """
    Decode the provided JWT token to extract the payload.

    :param token: The JWT token to decode.
    :return: The decoded payload if the token is valid and not expired, otherwise None.
    """
    try:
        decoded_token = jwt.decode(token, app_config.SECRET_KEY, algorithms=[app_config.ALGORITHM])
        # Check if the token is expired
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except jwt.ExpiredSignatureError:
        # Token has expired
        return {}
    except jwt.InvalidTokenError:
        # Token is invalid
        return {}


def verify_jwt(jwt_token: str) -> bool:
    """
    Verify the provided JWT token.

    :param jwt_token: The JWT token to verify.
    :return: True if the token is valid, False otherwise.
    """
    is_token_valid: bool = False
    try:
        payload = decode_jwt(jwt_token)
    except:
        payload = None
    if payload:
        is_token_valid = True
    return is_token_valid


class JWTBearer(HTTPBearer):
    """
    A class to validate JWT tokens in API requests.

    This class extends HTTPBearer to handle JWT token validation.
    """

    def __init__(self, auto_error: bool = True):
        """
        Initialize the JWTBearer instance.

        :param auto_error: Whether to automatically raise errors on invalid tokens.
        """
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        """
        Validate the JWT token in the incoming request.

        :param request: The incoming request object.
        :return: The JWT token if valid.
        :raises HTTPException: If the token is invalid or expired.
        """
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            # Check if the authentication scheme is Bearer
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            # Verify the JWT token
            if not verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")
