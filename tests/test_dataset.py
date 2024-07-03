from fastapi import status

from app.helper import get_password_hash


def get_token(test_client, mock_db):
    # Insert a user into the mock database and get jwt token by sign in
    mock_db["user"].insert_one({"email": "user@example.com", "password": get_password_hash("hashed-password")})

    response = test_client.post(
        "/auth/sign-in",
        json={"email": "user@example.com", "password": "hashed-password"}
    )

    return response.json()["token"]


# Sample unit test for the upload dataset endpoint
def test_upload_dataset_csv(test_client, mock_db):
    # get jwt token
    token = get_token(test_client, mock_db)

    with open("tests/sample.csv", "rb") as file:
        response = test_client.post(
            "/datasets/upload",
            files={"file": ("sample.csv", file, "text/csv")},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "code": status.HTTP_200_OK,
        "message": "Upload successfully"
    }


def test_upload_dataset_invalid_file_type(test_client, mock_db):
    # get jwt token
    token = get_token(test_client, mock_db)

    with open("tests/sample.txt", "rb") as file:
        response = test_client.post(
            "/datasets/upload",
            files={"file": ("sample.txt", file, "text/plain")},
            headers={
                "Authorization": f"Bearer {token}"
            }
        )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {
        "code": status.HTTP_400_BAD_REQUEST,
        "message": "Invalid file type. Only CSV files are allowed."
    }


def test_get_all_datasets(test_client, mock_db):
    # get jwt token
    token = get_token(test_client, mock_db)

    response = test_client.get(
        "/datasets",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_get_dataset_by_id(test_client, mock_db):
    # get jwt token
    token = get_token(test_client, mock_db)

    dataset_id = "some_id"
    response = test_client.get(
        f"/datasets/{dataset_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR  # Assuming ID doesn't exist
    assert response.json()["code"] == status.HTTP_500_INTERNAL_SERVER_ERROR


def test_delete_dataset(test_client, mock_db):
    # get jwt token
    token = get_token(test_client, mock_db)

    dataset_id = "some_id"
    response = test_client.delete(
        f"/datasets/{dataset_id}",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR  # Assuming ID doesn't exist
    assert response.json()["code"] == status.HTTP_500_INTERNAL_SERVER_ERROR
