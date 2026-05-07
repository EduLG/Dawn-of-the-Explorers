from datetime import datetime
from ..extensions import db


class Exploration(db.Model):
    __tablename__ = 'exploration'

    id         = db.Column(db.Integer, primary_key=True)
    party_id   = db.Column(db.Integer, db.ForeignKey('party.id', ondelete='CASCADE'), nullable=False)
    dungeon_id = db.Column(db.Integer, db.ForeignKey('dungeon.id'), nullable=False)
    started_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ends_at    = db.Column(db.DateTime, nullable=False)
    status     = db.Column(db.String, nullable=False, default='in_progress')
    result     = db.Column(db.JSON)

    party   = db.relationship('Party', backref='explorations')
    dungeon = db.relationship('Dungeon')
