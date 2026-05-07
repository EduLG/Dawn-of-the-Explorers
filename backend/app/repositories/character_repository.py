from app.extensions import db
from app.models.character import Character
from app.models.character_equipment import CharacterEquipment


def get_character_by_id(character_id):
    return Character.query.filter_by(id=character_id).first()


def update_character_job(character_id, job_id):
    character = get_character_by_id(character_id)
    character.current_job_id = job_id
    db.session.commit()


def unequip_all(character_id):
    CharacterEquipment.query.filter_by(character_id=character_id).delete()
    db.session.commit()
