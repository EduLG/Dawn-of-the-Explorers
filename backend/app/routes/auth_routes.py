from flask import Blueprint
from app.handlers.auth_handler import register_user_handler, login_user_handler, refresh_token_handler

auth_bp = Blueprint("auth", __name__)

# delegate to handler functions (route -> handler -> service -> repository)

#Register
auth_bp.route("/register", methods=["POST"])(register_user_handler)

#Login
auth_bp.route("/login", methods=["POST"])(login_user_handler)

#Token refresh
auth_bp.route("/refresh", methods=["POST"])(refresh_token_handler)

