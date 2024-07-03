"""
This module provides functions to interact with the dataset collection in the MongoDB database.
"""

from bson.objectid import ObjectId
from datetime import datetime


def insert_dataset(collection, filename: str, size: int, content: str) -> None:
    """
    Insert a new dataset document into the collection.

    :param collection: The mongo db collection.
    :param filename: The name of the dataset file.
    :param size: The size of the dataset file.
    :param content: The content of the dataset file.
    """
    collection.insert_one({
        "filename": filename,
        "size": size,
        "content": content,
        "upload_date": datetime.now()  # Store the current date and time as the upload date
    })


def get_all_datasets(collection) -> list:
    """
    Retrieve all datasets from the collection without the content field.

    :param collection: The mongo db collection.
    :return: A list of dictionaries containing dataset metadata.
    """
    return [{
        "id": str(dataset.get("_id")),  # Convert ObjectId to string for JSON serialization
        "filename": dataset.get("filename"),
        "size": dataset.get("size"),
        "upload_date": dataset.get("upload_date")
    } for dataset in collection.find({}, {"content": 0})]  # Exclude the content field


def get_dataset_by_id(collection, dataset_id: str) -> dict:
    """
    Retrieve a dataset by its ObjectId.

    :param collection: The mongo db collection.
    :param dataset_id: The ObjectId of the dataset as a string.
    :return: A dictionary containing the dataset content or None if not found.
    """
    return collection.find_one({"_id": ObjectId(dataset_id)}, {"content": 1})  # Only include the content field


def delete_dataset_by_id(collection, dataset_id: str) -> None:
    """
    Delete a dataset by its ObjectId.

    :param collection: The mongo db collection.
    :param dataset_id: The ObjectId of the dataset as a string.
    """
    collection.delete_one({"_id": ObjectId(dataset_id)})  # Perform the deletion
