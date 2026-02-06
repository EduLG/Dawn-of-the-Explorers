from ..extensions import db

class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    icon = db.Column(db.String, nullable=False)

    characters = db.relationship('Character', back_populates='current_job')
    equipment = db.relationship('JobEquipment', back_populates='job', cascade='all, delete-orphan')
