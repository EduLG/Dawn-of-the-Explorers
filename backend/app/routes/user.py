from flask import Blueprint
from app.handlers.user_handler import get_user_handler

user_bp = Blueprint("user", __name__)

user_bp.route("/<int:user_id>", methods=["GET"])(get_user_handler)
