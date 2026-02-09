from flask import Blueprint
from app.handlers.auth_handler import register_user_handler, login_user_handler

auth_bp = Blueprint("auth", __name__)

# delegate to handler functions (route -> handler -> service -> repository)
auth_bp.route("/register", methods=["POST"])(register_user_handler)
auth_bp.route("/login", methods=["POST"])(login_user_handler)

