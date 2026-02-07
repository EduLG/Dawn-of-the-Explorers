from flask import Flask
from app.routes.auth import auth_bp
from app.routes.user import user_bp
from flask_cors import CORS
from .extensions import db
from config import Config
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.config["JWT_SECRET_KEY"] = "super_secret_key"
    jwt = JWTManager(app)

    CORS(app)
    db.init_app(app)

    from app.models.user import User
    from app.models.party import Party
    from app.models.party_character import PartyCharacter
    from app.models.character import Character
    from app.models.job import Job
    from app.models.equipment import Equipment
    from app.models.character_equipment import CharacterEquipment
    from app.models.job_equipment import JobEquipment


    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/users")

    return app
