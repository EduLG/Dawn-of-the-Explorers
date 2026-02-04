from . import db
from .job import Job
from .character_job import CharacterJob
from .character_equipment import CharacterEquipment
from .party_character import PartyCharacter

class Character(db.Model):
    __tablename__ = 'character'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    current_job_id = db.Column(db.Integer, db.ForeignKey('job.id'))

    current_job = db.relationship('Job', back_populates='characters')
    jobs = db.relationship('CharacterJob', back_populates='character', cascade='all, delete-orphan')
    equipment = db.relationship('CharacterEquipment', back_populates='character', cascade='all, delete-orphan')
    party_entries = db.relationship('PartyCharacter', back_populates='character')
