from ..extensions import db

class CharacterJob(db.Model):
    __tablename__ = 'character_job'

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)

    character = db.relationship('Character', back_populates='jobs')
    job = db.relationship('Job', back_populates='character_jobs')
