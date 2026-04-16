from app.extensions import db
from app.models.equipment import Equipment
from app.models.character_equipment import CharacterEquipment


def get_equipment_by_job(job_id):
    return Equipment.query.filter_by(job_id=job_id).all()


def get_equipment_by_id(equipment_id):
    return Equipment.query.filter_by(id=equipment_id).first()


def get_character_equipment_by_slot(character_id, slot):
    return CharacterEquipment.query.filter_by(character_id=character_id, slot=slot).first()


def update_character_equipment(character_id, slot, equipment_id):
    record = get_character_equipment_by_slot(character_id, slot)
    if record:
        record.equipment_id = equipment_id
    else:
        record = CharacterEquipment(character_id=character_id, slot=slot, equipment_id=equipment_id)
        db.session.add(record)
    db.session.commit()
