from flask import jsonify
from flask_jwt_extended import jwt_required

from app.services.auth_service import ServiceError
from app.services.job_service import get_jobs


@jwt_required()
def get_jobs_handler():
    try:
        result = get_jobs()
        return jsonify(result), 200
    except ServiceError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
