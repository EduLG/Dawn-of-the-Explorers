from . import db
from .character_equipment import CharacterEquipment

class Equipment(db.Model):
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, default=0)

    equipped_by = db.relationship('CharacterEquipment', back_populates='equipment', cascade='all, delete-orphan')
