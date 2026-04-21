from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.auth_service import ServiceError
from app.services.inventory_service import get_inventory, equip_from_inventory


@jwt_required()
def get_inventory_handler():
    user_id = get_jwt_identity()
    try:
        result = get_inventory(user_id)
        return jsonify(result), 200
    except ServiceError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@jwt_required()
def equip_from_inventory_handler(inventory_id):
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    character_id = data.get("character_id")
    slot = data.get("slot")

    if not character_id or not slot:
        return jsonify({"error": "character_id and slot are required"}), 400

    try:
        equip_from_inventory(user_id, inventory_id, character_id, slot)
        return jsonify({"message": "Item equipped from inventory"}), 200
    except ServiceError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
