from flask import Blueprint
from app.handlers.party_handler import setup_party_handler

party_bp = Blueprint("party", __name__)

party_bp.route("/setup", methods=["POST"])(setup_party_handler)
