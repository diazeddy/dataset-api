"""
This module defines the authentication routes for user sign-up and sign-in.
"""

from fastapi import APIRouter, status, Depends
from fastapi.responses import JSONResponse

from app.schemas.UserSchema import UserTokenResponse, UserRequest
from app.schemas.GlobalSchema import MessageResponse
from app.database import get_database
from app.helper import get_password_hash, generate_jwt, verify_password
from app.controllers.UserController import is_user_exist, insert_new_user, get_user_by_email

auth_router = APIRouter()


@auth_router.post(
    "/sign-up",
    response_model=UserTokenResponse,
    responses={
        409: {"model": MessageResponse}
    },
    status_code=status.HTTP_201_CREATED,
    tags=["auth"]
)
async def sign_up(user: UserRequest, database=Depends(get_database)):
    """
    Register a new user.

    :param database: The mongo db database
    :param user: The user details for registration.
    :return: A JSON response containing a JWT token or an error message if the user already exists.
    """
    # Check if the user already exists
    if is_user_exist(database["user"], user.email):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "code": status.HTTP_409_CONFLICT,
                "message": "User already exists"
            }
        )

    # Hash the user's password
    hashed_password = get_password_hash(user.password)

    # Insert the new user into the database
    insert_new_user(database["user"], user.email, hashed_password)

    # Return a JWT token for the newly registered user
    return {"token": generate_jwt(user.email)}


@auth_router.post(
    "/sign-in",
    response_model=UserTokenResponse,
    responses={
        401: {"model": MessageResponse}
    },
    status_code=status.HTTP_200_OK,
    tags=["auth"]
)
async def sign_in(user: UserRequest, database=Depends(get_database)):
    """
    Authenticate an existing user.

    :param database: The mongo db database
    :param user: The user details for authentication.
    :return: A JSON response containing a JWT token or an error message if authentication fails.
    """
    # Retrieve the user from the database by email
    db_user = get_user_by_email(database["user"], user.email)

    # Verify the provided password with the stored hashed password
    if db_user and verify_password(user.password, db_user.get("password")):
        # Return a JWT token if authentication is successful
        return {"token": generate_jwt(user.email)}
    else:
        # Return an error message if authentication fails
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "code": status.HTTP_401_UNAUTHORIZED,
                "message": "Invalid email or password."
            }
        )
