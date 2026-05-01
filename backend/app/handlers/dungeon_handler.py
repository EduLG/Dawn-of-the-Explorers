from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.auth_service import ServiceError
from app.services.dungeon_service import get_dungeons, explore_dungeon


@jwt_required()
def get_dungeons_handler():
    user_id = get_jwt_identity()
    try:
        result = get_dungeons(user_id)
        return jsonify(result), 200
    except ServiceError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


@jwt_required()
def explore_dungeon_handler(dungeon_id):
    user_id = get_jwt_identity()
    try:
        result = explore_dungeon(user_id, dungeon_id)
        return jsonify(result), 200
    except ServiceError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
