from . import db
from .party import Party

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    party_id = db.Column(db.Integer, db.ForeignKey('party.id'), unique=True)
    party = db.relationship('Party', back_populates='user', uselist=False)
