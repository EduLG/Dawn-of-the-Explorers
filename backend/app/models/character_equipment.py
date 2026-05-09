from ..extensions import db

class CharacterEquipment(db.Model):
    __tablename__ = 'character_equipment'

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id', ondelete='CASCADE'), nullable=False)
    inventory_id = db.Column(db.Integer, db.ForeignKey('party_inventory.id', ondelete='CASCADE'), nullable=False)
    slot = db.Column(db.String, nullable=False)

    character = db.relationship('Character', back_populates='equipment')
    inventory_item = db.relationship('PartyInventory', back_populates='character_equipment')

    @property
    def equipment(self):
        return self.inventory_item.equipment if self.inventory_item else None

    __table_args__ = (
        db.UniqueConstraint('character_id', 'slot', name='uix_character_slot'),
        db.CheckConstraint(
            "slot IN ('head', 'chest', 'primary_hand', 'secondary_hand', 'accesory')",
            name="ck_character_equipment_slot",
        ),
    )
