from ..extensions import db

class Party(db.Model):
    __tablename__ = 'party'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)

    # FK to User — Party is the child in the 1:1 relationship
    user_id = db.Column(db.String(36), db.ForeignKey('user.id', ondelete='CASCADE'), unique=True, nullable=False)
    user = db.relationship('User', back_populates='party')

    # 1:N with Character
    characters = db.relationship('Character', back_populates='party', cascade='all, delete-orphan', order_by='Character.id')

    # 1:N with PartyInventory
    inventory = db.relationship('PartyInventory', back_populates='party', cascade='all, delete-orphan')
