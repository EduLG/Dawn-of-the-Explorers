from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from app.repositories.auth_repository import (
    get_user_by_username,
    get_user_by_email,
    create_user,
)


class ServiceError(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code


def register_user(username, email, password):
    if not username or not email or not password:
        raise ServiceError("Missing data", 400)

    if get_user_by_username(username):
        raise ServiceError("The user already exists", 409)

    if get_user_by_email(email):
        raise ServiceError("The email already exists", 409)

    hashed = generate_password_hash(password)
    user = create_user(username, email, hashed)
    return user


def authenticate_user(username, password):
    if not username or not password:
        raise ServiceError("Missing data", 400)

    user = get_user_by_username(username)
    if not user:
        raise ServiceError("Invalid user", 401)

    if not check_password_hash(user.password, password):
        raise ServiceError("Invalid pass", 401)

    access_token = create_access_token(identity=user.id)
    return {"access_token": access_token, "user_id": user.id, "username": user.username}
