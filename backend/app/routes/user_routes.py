from flask import Blueprint

from app.handlers.user_handler import get_current_user_handler

user_bp = Blueprint("user", __name__)

user_bp.route("/me", methods=["GET"])(get_current_user_handler)
