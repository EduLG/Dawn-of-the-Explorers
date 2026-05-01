from flask import Flask
from app.routes.auth_routes import auth_bp
from app.routes.user_routes import user_bp
from app.routes.equipment_routes import equipment_bp
from app.routes.inventory_routes import inventory_bp
from flask_cors import CORS
from .extensions import db
from config import Config
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    jwt = JWTManager(app)

    CORS(app)
    db.init_app(app)

    from app.models.user import User
    from app.models.party import Party
    from app.models.character import Character
    from app.models.job import Job
    from app.models.equipment import Equipment
    from app.models.character_equipment import CharacterEquipment
    from app.models.party_inventory import PartyInventory
    from app.models.dungeon import Dungeon

    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(user_bp, url_prefix="/api/v1/users")
    app.register_blueprint(equipment_bp, url_prefix="/api/v1/equipment")
    app.register_blueprint(inventory_bp, url_prefix="/api/v1/inventory")

    return app
