from fastapi import status
from conftest import mock_db
from app.helper import get_password_hash


def test_sign_up_existing_user(test_client, mock_db):
    """
    Test signing up with an existing user.
    """
    # Insert a user into the mock database
    mock_db["user"].insert_one({"email": "existing@example.com", "password": "hashed-password"})

    # Try to sign up with the existing user's email
    response = test_client.post(
        "/auth/sign-up",
        json={"email": "existing@example.com", "password": "newpassword"}
    )

    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {
        "code": status.HTTP_409_CONFLICT,
        "message": "User already exists"
    }


def test_sign_up_new_user(test_client, mock_db):
    """
    Test signing up with a new user.
    """
    response = test_client.post(
        "/auth/sign-up",
        json={"email": "newuser@example.com", "password": "newpassword"}
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "token" in response.json()


def test_sign_in_success(test_client, mock_db):
    """
    Test successful sign-in.
    """
    # Insert a user into the mock database
    mock_db["user"].insert_one({"email": "user@example.com", "password": get_password_hash("hashed-password")})

    response = test_client.post(
        "/auth/sign-in",
        json={"email": "user@example.com", "password": "hashed-password"}
    )

    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.json()


def test_sign_in_invalid_credentials(test_client, mock_db):
    """
    Test sign-in with invalid credentials.
    """
    # Insert a user into the mock database
    mock_db["user"].insert_one({"email": "user@example.com", "password": get_password_hash("hashed-password")})

    response = test_client.post(
        "/auth/sign-in",
        json={"email": "user@example.com", "password": "wrong-password"}
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert response.json() == {
        "code": status.HTTP_401_UNAUTHORIZED,
        "message": "Invalid email or password."
    }
