from ..extensions import db

class PartyCharacter(db.Model):
    __tablename__ = 'party_character'

    id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    party_slot = db.Column(db.Integer, nullable=False)

    party = db.relationship('Party', back_populates='characters')
    character = db.relationship('Character', back_populates='party_entries')

    __table_args__ = (
        db.UniqueConstraint('party_id', 'party_slot', name='uix_party_slot'),
    )
