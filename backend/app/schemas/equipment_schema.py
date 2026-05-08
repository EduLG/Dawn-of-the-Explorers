from marshmallow import Schema, fields


class EquipmentSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    slot = fields.Str()
    rating = fields.Int()
    equipment_type = fields.Str()
