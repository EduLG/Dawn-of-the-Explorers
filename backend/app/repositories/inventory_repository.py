from app.extensions import db
from app.models.party_inventory import PartyInventory


def get_party_inventory(party_id):
    return PartyInventory.query.filter_by(party_id=party_id).all()


def get_inventory_item(inventory_id):
    return PartyInventory.query.get(inventory_id)


def add_to_inventory(party_id, equipment_id):
    item = PartyInventory(party_id=party_id, equipment_id=equipment_id)
    db.session.add(item)
    db.session.commit()
    return item


def remove_from_inventory(inventory_id):
    item = PartyInventory.query.get(inventory_id)
    if item:
        db.session.delete(item)
        db.session.commit()
