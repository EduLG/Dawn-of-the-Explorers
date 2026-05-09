from app.extensions import db
from app.models.equipment import Equipment
from app.models.character_equipment import CharacterEquipment
from app.models.party_inventory import PartyInventory


def get_equipment_by_type(equipment_type):
    return Equipment.query.filter_by(equipment_type=equipment_type).all()


def get_equipment_by_id(equipment_id):
    return Equipment.query.filter_by(id=equipment_id).first()


def get_character_equipment_by_slot(character_id, slot):
    return CharacterEquipment.query.filter_by(character_id=character_id, slot=slot).first()


def update_character_equipment(character_id, slot, inventory_id):
    record = get_character_equipment_by_slot(character_id, slot)
    if record:
        record.inventory_id = inventory_id
    else:
        record = CharacterEquipment(character_id=character_id, slot=slot, inventory_id=inventory_id)
        db.session.add(record)
    db.session.commit()


def unequip_by_inventory_id(inventory_id):
    CharacterEquipment.query.filter_by(inventory_id=inventory_id).delete()
    db.session.commit()


def unequip_by_equipment_and_party(equipment_id, party_id):
    records = (
        CharacterEquipment.query
        .join(PartyInventory, CharacterEquipment.inventory_id == PartyInventory.id)
        .filter(
            PartyInventory.party_id == party_id,
            PartyInventory.equipment_id == equipment_id,
        )
        .all()
    )
    for record in records:
        db.session.delete(record)
    db.session.commit()
