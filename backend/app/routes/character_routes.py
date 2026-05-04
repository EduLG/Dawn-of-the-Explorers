from flask import Blueprint
from app.handlers.character_handler import change_job_handler

character_bp = Blueprint("characters", __name__)

character_bp.route("/<int:character_id>/job", methods=["PATCH"])(change_job_handler)
