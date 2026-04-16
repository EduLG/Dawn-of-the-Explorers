from flask import Blueprint
from app.handlers.equipment_handler import (
    get_equipment_by_job_handler,
    update_character_equipment_handler,
)

equipment_bp = Blueprint("equipment", __name__)

#GET equipment
equipment_bp.route("", methods=["GET"])(get_equipment_by_job_handler)

#PUT Equipment by CharID
equipment_bp.route("/character/<int:character_id>", methods=["PUT"])(update_character_equipment_handler)
