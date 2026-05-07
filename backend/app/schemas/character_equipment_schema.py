from marshmallow import Schema, fields
from .equipment_schema import EquipmentSchema


class CharacterEquipmentSchema(Schema):
    slot = fields.Str()
    equipment = fields.Nested(EquipmentSchema)
