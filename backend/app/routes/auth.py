from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from app.extensions import db
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

# ---------------------------------------------------------------REGISTER

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if data is None:
        return jsonify({"error": "There is no data"}), 400

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "Missing data"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "The user already exists"}), 409
    
    if User.query.filter_by(email=email).first():
        return jsonify({"error":"The email already exists"}), 409

    hashed_password = generate_password_hash(password)

    new_user = User(
        username=username,
        email=email,
        password=hashed_password
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully."}), 201

#------------------------------------------------------------------LOGIN

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
        return jsonify({"error": "Missing data."}), 400
    
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"error": "Invalid user"}), 401
    
    if not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid pass"}), 401
    
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "user_id": user.id,
        "username": user.username
    }), 200
    