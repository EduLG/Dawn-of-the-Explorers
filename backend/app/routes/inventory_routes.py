from flask import Blueprint
from app.handlers.inventory_handler import (
    get_inventory_handler,
    equip_from_inventory_handler,
)

inventory_bp = Blueprint("inventory", __name__)

inventory_bp.route("", methods=["GET"])(get_inventory_handler)
inventory_bp.route("/<int:inventory_id>/equip", methods=["POST"])(equip_from_inventory_handler)
