"""
This module defines the Pydantic schemas used for user authentication.
"""

from pydantic import BaseModel, EmailStr


class UserRequest(BaseModel):
    """
    Schema for user registration and authentication requests.

    Attributes:
        email (EmailStr): The user's email address.
        password (str): The user's password.
    """
    email: EmailStr
    password: str


class UserTokenResponse(BaseModel):
    """
    Schema for user authentication response containing a JWT token.

    Attributes:
        token (str): The JWT token provided to the authenticated user.
    """
    token: str
