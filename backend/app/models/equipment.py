from ..extensions import db

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

    equipped_by = db.relationship('CharacterEquipment', back_populates='equipment', cascade='all, delete-orphan')
    allowed_jobs = db.relationship('JobEquipment', back_populates='equipment', cascade='all, delete-orphan')

    __table_args__ = (
        db.CheckConstraint(
            "type IN ('head', 'chest', 'primary hand', 'secondary hand', 'accesory')",
            name="ck_equipment_type",
        ),
    )