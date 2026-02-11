from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.services.auth_service import ServiceError
from app.services.user_service import get_user_profile


@jwt_required()
def get_current_user_handler():
    user_id = get_jwt_identity()

    try:
        profile = get_user_profile(user_id)
        return jsonify(profile), 200
    except ServiceError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
