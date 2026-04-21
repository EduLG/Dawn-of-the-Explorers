from ..extensions import db

class Party(db.Model):
    __tablename__ = 'party'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, default=1)
    experience = db.Column(db.Integer, default=0)

    # 1:1 with User
    user = db.relationship('User', back_populates='party', uselist=False)

    # 1:N with Character
    characters = db.relationship('Character', back_populates='party', cascade='all, delete-orphan')

    # 1:N with PartyInventory
    inventory = db.relationship('PartyInventory', back_populates='party', cascade='all, delete-orphan')
