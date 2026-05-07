from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.auth_service import ServiceError
from app.services.character_service import change_character_job


@jwt_required()
def change_job_handler(character_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    job_id = data.get("job_id") if data else None
    if not job_id:
        return jsonify({"error": "job_id is required"}), 400

    try:
        change_character_job(user_id, character_id, job_id)
        return jsonify({"message": "Job updated"}), 200
    except ServiceError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
