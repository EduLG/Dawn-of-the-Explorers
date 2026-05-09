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
    equipped = fields.Method("get_equipped")

    def get_equipped(self, obj):
        return obj.character_equipment is not None
