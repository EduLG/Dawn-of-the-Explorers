from ..extensions import db

EQUIPMENT_SLOTS = ("head", "chest", "primary_hand", "secondary_hand", "accesory")
ARMOR_TYPES = ("plate", "leather", "cloth")

JOB_ARMOR_TYPE = {
    "warrior": "plate", "fender": "plate",
    "adventurer": "leather", "beastmaster": "leather",
    "gunslinger": "leather", "thief": "leather",
    "alchemist": "cloth", "engineer": "cloth",
    "sage": "cloth", "scholar": "cloth",
}

class Equipment(db.Model):
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    slot = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, default=0)
    equipment_type = db.Column(db.String, nullable=False)

    # M:N with Character through CharacterEquipment
    equipped_by = db.relationship('CharacterEquipment', back_populates='equipment', cascade='all, delete-orphan')

    # 1:N with PartyInventory
    in_inventories = db.relationship('PartyInventory', back_populates='equipment', cascade='all, delete-orphan')

    __table_args__ = (
        db.CheckConstraint(
            "slot IN ('head', 'chest', 'primary_hand', 'secondary_hand', 'accesory')",
            name="ck_equipment_slot",
        ),
        db.CheckConstraint(
            "equipment_type IN ('plate', 'leather', 'cloth')",
            name="ck_equipment_armor_type",
        ),
    )
