from flask import Blueprint
from app.handlers.equipment_handler import get_equipment_by_job_handler

equipment_bp = Blueprint("equipment", __name__)

equipment_bp.route("", methods=["GET"])(get_equipment_by_job_handler)
