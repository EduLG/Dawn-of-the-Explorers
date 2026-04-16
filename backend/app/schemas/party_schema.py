from marshmallow import Schema, fields
from .character_schema import CharacterSchema
from app.services.party_service import calculate_party_rating


class PartySchema(Schema):
    id = fields.Int()
    name = fields.Str()
    level = fields.Int()
    experience = fields.Int()
    rating = fields.Method("get_rating")
    characters = fields.List(fields.Nested(CharacterSchema))

    def get_rating(self, obj):
        return calculate_party_rating(obj.characters)
