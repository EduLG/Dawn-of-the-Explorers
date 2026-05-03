from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.auth_service import ServiceError
from app.services.party_setup_service import setup_party


@jwt_required()
def setup_party_handler():
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    party_name = data.get("party_name")
    characters_data = data.get("characters")

    if not party_name or not isinstance(characters_data, list):
        return jsonify({"error": "party_name and characters are required"}), 400

    try:
        setup_party(user_id, party_name, characters_data)
        return jsonify({"message": "Party set up successfully"}), 200
    except ServiceError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
