"""
This module defines the Pydantic schemas used for dataset responses.
"""

from pydantic import BaseModel
from datetime import datetime


class DatasetListResponse(BaseModel):
    """
    Schema for listing datasets.

    Attributes:
        id (str): The unique identifier of the dataset.
        filename (str): The name of the uploaded file.
        size (int): The size of the uploaded file in bytes.
        upload_date (datetime): The date and time when the dataset was uploaded.
    """
    id: str
    filename: str
    size: int
    upload_date: datetime


class DatasetDetailResponse(BaseModel):
    """
    Schema for retrieving a specific dataset's content.

    Attributes:
        content (str): The content of the dataset, typically in JSON format.
    """
    content: str
