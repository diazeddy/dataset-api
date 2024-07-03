"""
This module defines the routes for dataset operations such as uploading, retrieving, and deleting datasets.
"""

from fastapi import APIRouter, UploadFile, status, Depends
from fastapi.responses import JSONResponse
from io import StringIO
from typing import List

import json
import pandas as pd

from app.schemas.DatasetSchema import DatasetListResponse, DatasetDetailResponse
from app.schemas.GlobalSchema import MessageResponse
from app.controllers.DatasetController import (
    insert_dataset,
    get_dataset_by_id,
    get_all_datasets,
    delete_dataset_by_id
)
from app.helper import JWTBearer
from app.database import get_database

dataset_router = APIRouter(dependencies=[Depends(JWTBearer())])


@dataset_router.post(
    "/upload",
    response_model=MessageResponse,
    responses={
        400: {"model": MessageResponse},
        500: {"model": MessageResponse}
    },
    status_code=status.HTTP_200_OK,
    tags=["datasets"]
)
async def upload_dataset(file: UploadFile, database=Depends(get_database)):
    """
    Upload a new dataset in CSV format.

    :param database: The mongo db database
    :param file: The CSV file to upload.
    :return: A JSON response indicating success or failure.
    """
    # Check if the uploaded file is a CSV
    if file.content_type != 'text/csv':
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "code": status.HTTP_400_BAD_REQUEST,
                "message": "Invalid file type. Only CSV files are allowed."
            }
        )

    try:
        # Read the CSV file
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))

        # Convert DataFrame to dictionary and insert into MongoDB
        data = df.to_dict(orient="records")
        insert_dataset(database["dataset"], file.filename, file.size, json.dumps(data))

        return {
            "code": status.HTTP_200_OK,
            "message": "Upload successfully"
        }

    except Exception as e:
        # Handle any exceptions that occur during file processing or data insertion
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            }
        )


@dataset_router.get(
    "",
    response_model=List[DatasetListResponse],
    responses={
        500: {"model": MessageResponse}
    },
    status_code=status.HTTP_200_OK,
    tags=["datasets"]
)
async def get_all_datasets_route(database=Depends(get_database)):
    """
    Retrieve all datasets.

    :param database: The mongo db database
    :return: A list of dataset metadata.
    """
    try:
        # Fetch all datasets from the database
        return get_all_datasets(database["dataset"])
    except Exception as e:
        # Handle any exceptions that occur during data retrieval
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            }
        )


@dataset_router.get(
    "/{dataset_id}",
    response_model=DatasetDetailResponse,
    responses={
        500: {"model": MessageResponse}
    },
    status_code=status.HTTP_200_OK,
    tags=["datasets"]
)
async def get_dataset(dataset_id: str, database=Depends(get_database)):
    """
    Retrieve a specific dataset by its ID.

    :param database: The mongo db database
    :param dataset_id: The ID of the dataset to retrieve.
    :return: The dataset content or an error message if not found.
    """
    try:
        # Fetch the dataset from the database by its ID
        return get_dataset_by_id(database["dataset"], dataset_id)
    except Exception as e:
        # Handle any exceptions that occur during data retrieval
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            }
        )


@dataset_router.delete(
    "/{dataset_id}",
    response_model=MessageResponse,
    responses={
        500: {"model": MessageResponse}
    },
    status_code=status.HTTP_200_OK,
    tags=["datasets"]
)
async def delete_dataset(dataset_id: str, database=Depends(get_database)):
    """
    Delete a specific dataset by its ID.

    :param database: The mongo db database
    :param dataset_id: The ID of the dataset to delete.
    :return: A JSON response indicating success or failure.
    """
    try:
        # Delete the dataset from the database by its ID
        delete_dataset_by_id(database["dataset"], dataset_id)
        return {
            "code": status.HTTP_200_OK,
            "message": "Dataset deleted successfully"
        }
    except Exception as e:
        # Handle any exceptions that occur during data deletion
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            }
        )
