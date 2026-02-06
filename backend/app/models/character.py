from ..extensions import db

class Character(db.Model):
    __tablename__ = 'character'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    current_job_id = db.Column(db.Integer, db.ForeignKey('job.id'))

    current_job = db.relationship('Job', back_populates='characters')
    party_entries = db.relationship('PartyCharacter', back_populates='character')
