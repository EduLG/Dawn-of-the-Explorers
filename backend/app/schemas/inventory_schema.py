from marshmallow import Schema, fields


class InventoryEquipmentSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    type = fields.Str()
    rating = fields.Int()
    job_id = fields.Int()
    job_name = fields.Method("get_job_name")

    def get_job_name(self, obj):
        return obj.job.name if obj.job else None


class PartyInventorySchema(Schema):
    id = fields.Int()
    equipment = fields.Nested(InventoryEquipmentSchema)
