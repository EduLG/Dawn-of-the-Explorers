from flask import request, jsonify
from app.services.auth_service import register_user, authenticate_user, ServiceError


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
            "user_id": token_payload["user_id"],
            "username": token_payload["username"],
        }), 200
    except ServiceError as e:
        return jsonify({"error": str(e)}), e.status_code
    except Exception:
        return jsonify({"error": "Internal server error"}), 500
