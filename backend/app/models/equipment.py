from ..extensions import db

# Define allowed equipment types
EQUIPMENT_TYPES = (
    "head",
    "chest",
    "primary hand",
    "secondary hand",
    "accesory",
)

class Equipment(db.Model):
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, default=0)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    # Backref to Job
    job = db.relationship('Job', back_populates='equipments')

    # M:N with Character through CharacterEquipment
    equipped_by = db.relationship('CharacterEquipment', back_populates='equipment', cascade='all, delete-orphan')

    # 1:N with PartyInventory
    in_inventories = db.relationship('PartyInventory', back_populates='equipment', cascade='all, delete-orphan')

    # Constraint to ensure type is one of the allowed values
    __table_args__ = (
        db.CheckConstraint(
            "type IN ('head', 'chest', 'primary_hand', 'secondary_hand', 'accesory')",
            name="ck_equipment_type",
        ),
    )
