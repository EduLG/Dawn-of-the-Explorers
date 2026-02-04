from app import create_app
from app.extensions import db

from app.models.user import User
from app.models.party import Party
from app.models.party_character import PartyCharacter
from app.models.character import Character
from app.models.job import Job
from app.models.character_job import CharacterJob
from app.models.equipment import Equipment
from app.models.character_equipment import CharacterEquipment

app = create_app()

with app.app_context():
    db.create_all()
    print("Tables created successfully")
