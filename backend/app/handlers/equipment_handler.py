from flask import request, jsonify
from flask_jwt_extended import jwt_required

from app.services.auth_service import ServiceError
from app.services.equipment_service import get_equipment_by_type


@jwt_required()
def get_equipment_by_type_handler():
    equipment_type = request.args.get("equipment_type")

    try:
        result = get_equipment_by_type(equipment_type)
        return jsonify(result), 200
    except ServiceError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
