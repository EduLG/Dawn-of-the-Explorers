from ..extensions import db

class Character(db.Model):
    __tablename__ = 'character'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    party_id = db.Column(db.Integer, db.ForeignKey('party.id', ondelete='CASCADE'), nullable=False)
    current_job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    party = db.relationship('Party', back_populates='characters')
    current_job = db.relationship('Job', back_populates='characters')

    # M:N with Equipment through CharacterEquipment
    equipment = db.relationship('CharacterEquipment', back_populates='character', cascade='all, delete-orphan')
