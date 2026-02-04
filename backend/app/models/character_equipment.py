from ..extensions import db
from .character import Character
from .equipment import Equipment

class CharacterEquipment(db.Model):
    __tablename__ = 'character_equipment'

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    slot = db.Column(db.String, nullable=False)

    character = db.relationship('Character', back_populates='equipment')
    equipment = db.relationship('Equipment', back_populates='equipped_by')

    __table_args__ = (
        db.UniqueConstraint('character_id', 'slot', name='uix_character_slot'),
    )
