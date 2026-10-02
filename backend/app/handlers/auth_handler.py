from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services.auth_service import (
    register_user,
    authenticate_user,
    create_demo_session,
    refresh_access_token,
    ServiceError,
)


def register_user_handler():
    data = request.get_json()
    if data is None:
        return jsonify({"error": "There is no data"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    try:
        register_user(username, email, password)
        return jsonify({"message": "User created successfully."}), 201
    except ServiceError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


def login_user_handler():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    username = data.get("username")
    password = data.get("password")

    try:
        token_payload = authenticate_user(username, password)
        return jsonify({
            "message": "Login successful",
            "access_token": token_payload["access_token"],
            "refresh_token": token_payload["refresh_token"],
            "user_id": token_payload["user_id"],
            "username": token_payload["username"],
        }), 200
    except ServiceError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception:
        return jsonify({"error": "Internal server error"}), 500


def demo_login_handler():
    try:
        payload = create_demo_session()
        return jsonify({
            "message": "Demo session started",
            "access_token": payload["access_token"],
            "refresh_token": payload["refresh_token"],
            "user_id": payload["user_id"],
            "username": payload["username"],
            "is_demo": True,
        }), 200
    except Exception:
        return jsonify({"error": "Could not start demo session"}), 500


@jwt_required(refresh=True)
def refresh_token_handler():
    new_access_token = refresh_access_token(get_jwt_identity(), get_jwt())
    return jsonify({"access_token": new_access_token}), 200
