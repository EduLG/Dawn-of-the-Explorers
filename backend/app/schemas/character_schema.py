from marshmallow import Schema, fields
from .job_schema import JobSchema
from .character_equipment_schema import CharacterEquipmentSchema
from app.services.character_service import calculate_character_rating


class CharacterSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    current_job = fields.Nested(JobSchema)
    equipped_items = fields.List(fields.Nested(CharacterEquipmentSchema), attribute="equipment")
    rating = fields.Method("get_rating")

    def get_rating(self, obj):
        return calculate_character_rating(obj.equipment)
