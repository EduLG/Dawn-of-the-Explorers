from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.auth_service import ServiceError
from app.services.equipment_service import get_equipment_by_job, update_character_equipment


@jwt_required()
def get_equipment_by_job_handler():
    job_id = request.args.get("job_id")

    try:
        result = get_equipment_by_job(job_id)
        return jsonify(result), 200
    except ServiceError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@jwt_required()
def update_character_equipment_handler(character_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    slot = data.get("slot")
    equipment_id = data.get("equipment_id")

    if not slot or not equipment_id:
        return jsonify({"error": "slot and equipment_id are required"}), 400

    try:
        update_character_equipment(user_id, character_id, slot, equipment_id)
        return jsonify({"message": "Equipment updated"}), 200
    except ServiceError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
