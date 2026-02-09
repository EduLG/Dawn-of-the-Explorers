from ..extensions import db

class Job(db.Model):
    __tablename__ = 'job'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    icon = db.Column(db.String, nullable=False)

    # 1:N with Character
    characters = db.relationship('Character', back_populates='current_job')

    # 1:N with Equipment
    equipments = db.relationship('Equipment', back_populates='job')
