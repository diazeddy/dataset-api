"""
This module defines the Pydantic schema used for uniform message responses.
"""

from pydantic import BaseModel


class MessageResponse(BaseModel):
    """
    Schema for standard message responses.

    Attributes:
        code (int): The HTTP status code of the response.
        message (str): A descriptive message related to the response.
    """
    code: int
    message: str
