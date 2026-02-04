from . import db
from .party_character import PartyCharacter
from .user import User

class Party(db.Model):
    __tablename__ = 'party'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)
    rating = db.Column(db.Integer, default=0)

    user = db.relationship('User', back_populates='party', uselist=False)
    characters = db.relationship('PartyCharacter', back_populates='party', cascade='all, delete-orphan')
