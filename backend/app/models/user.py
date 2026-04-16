from ..extensions import db
import uuid

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    # 1:1 relationship with Party
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'), unique=True, nullable=False)
    party = db.relationship('Party', back_populates='user', uselist=False)

