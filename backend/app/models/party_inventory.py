from ..extensions import db


class PartyInventory(db.Model):
    __tablename__ = 'party_inventory'

    id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('party.id', ondelete='CASCADE'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)

    party = db.relationship('Party', back_populates='inventory')
    equipment = db.relationship('Equipment', back_populates='in_inventories')
    character_equipment = db.relationship('CharacterEquipment', back_populates='inventory_item', uselist=False)
