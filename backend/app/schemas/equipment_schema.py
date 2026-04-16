from marshmallow import Schema, fields


class EquipmentSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    type = fields.Str()
    rating = fields.Int()
