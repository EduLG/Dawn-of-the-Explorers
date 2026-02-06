from ..extensions import db
from .job import Job
from .equipment import Equipment


class JobEquipment(db.Model):
    __tablename__ = 'job_equipment'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    slot = db.Column(db.String, nullable=False)

    job = db.relationship('Job', back_populates='equipment')
    equipment = db.relationship('Equipment', back_populates='job_assignments')

    __table_args__ = (
        db.UniqueConstraint('job_id', 'slot', name='uix_job_slot'),
    )
