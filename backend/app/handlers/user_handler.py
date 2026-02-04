from flask import jsonify, request
from app.services.user_service import get_user_profile
from app.services.auth_service import ServiceError


def get_user_handler(user_id):
	try:
		profile = get_user_profile(user_id)
		return jsonify(profile), 200
	except ServiceError as e:
		return jsonify({"error": str(e)}), e.status_code
	except Exception:
		return jsonify({"error": "Internal server error"}), 500

