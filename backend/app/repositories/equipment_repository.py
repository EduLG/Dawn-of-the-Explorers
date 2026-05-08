from app.extensions import db
from app.models.equipment import Equipment
from app.models.character_equipment import CharacterEquipment


def get_equipment_by_type(equipment_type):
    return Equipment.query.filter_by(equipment_type=equipment_type).all()


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


def is_equipment_on_other_character(equipment_id, party_id, exclude_character_id):
    from app.models.character import Character
    return (
        CharacterEquipment.query
        .join(Character, CharacterEquipment.character_id == Character.id)
        .filter(
            Character.party_id == party_id,
            CharacterEquipment.equipment_id == equipment_id,
            CharacterEquipment.character_id != exclude_character_id,
        )
        .first()
    ) is not None


def unequip_by_equipment_and_party(equipment_id, party_id):
    from app.models.character import Character
    records = (
        CharacterEquipment.query
        .join(Character, CharacterEquipment.character_id == Character.id)
        .filter(Character.party_id == party_id, CharacterEquipment.equipment_id == equipment_id)
        .all()
    )
    for record in records:
        db.session.delete(record)
    db.session.commit()
