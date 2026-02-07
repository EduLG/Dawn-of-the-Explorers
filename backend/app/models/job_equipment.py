from ..extensions import db

class JobEquipment(db.Model):
    __tablename__ = 'job_equipment'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'))
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'))

    job = db.relationship('Job', back_populates='job_equipment')
    equipment = db.relationship('Equipment', back_populates='allowed_jobs')

    __table_args__ = (db.UniqueConstraint('job_id', 'equipment_id', name='uix_job_equipment'),)