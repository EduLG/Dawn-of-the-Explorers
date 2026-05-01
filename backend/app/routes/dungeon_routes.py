from flask import Blueprint
from app.handlers.dungeon_handler import get_dungeons_handler, explore_dungeon_handler

dungeon_bp = Blueprint("dungeons", __name__)

dungeon_bp.route("", methods=["GET"])(get_dungeons_handler)
dungeon_bp.route("/<int:dungeon_id>/explore", methods=["POST"])(explore_dungeon_handler)
