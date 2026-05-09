from marshmallow import Schema, fields
from .equipment_schema import EquipmentSchema


class CharacterEquipmentSchema(Schema):
    slot = fields.Str()
    inventory_id = fields.Int()
    equipment = fields.Nested(EquipmentSchema)
