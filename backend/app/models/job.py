from . import db
from .character import Character
from .character_job import CharacterJob

class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    characters = db.relationship('Character', back_populates='current_job')
    character_jobs = db.relationship('CharacterJob', back_populates='job', cascade='all, delete-orphan')
