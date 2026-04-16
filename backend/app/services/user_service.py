from app.repositories.user_repository import get_user_by_id
from app.services.auth_service import ServiceError
from app.schemas import UserSchema


def get_user_profile(user_id):
    user = get_user_by_id(user_id)
    if not user:
        raise ServiceError("User not found", 404)

    return UserSchema().dump(user)
