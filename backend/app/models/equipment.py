from ..extensions import db

class Equipment(db.Model):
    __tablename__ = 'equipment'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    rating = db.Column(db.Integer, default=0)

    job_assignments = db.relationship('JobEquipment', back_populates='equipment', cascade='all, delete-orphan')
