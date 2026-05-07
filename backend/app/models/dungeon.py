from ..extensions import db


class Dungeon(db.Model):
    __tablename__ = 'dungeon'

    id                = db.Column(db.Integer, primary_key=True)
    name              = db.Column(db.String, nullable=False)
    description       = db.Column(db.String)
    image_path        = db.Column(db.String)
    min_rating        = db.Column(db.Integer, default=0, nullable=False)
    visibility_rating = db.Column(db.Integer, default=0, nullable=False)
    duration          = db.Column(db.Integer, default=60, nullable=False)
    loot              = db.Column(db.JSON)
