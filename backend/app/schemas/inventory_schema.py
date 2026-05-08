from marshmallow import Schema, fields


class InventoryEquipmentSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    slot = fields.Str()
    rating = fields.Int()
    equipment_type = fields.Str()


class PartyInventorySchema(Schema):
    id = fields.Int()
    equipment = fields.Nested(InventoryEquipmentSchema)
