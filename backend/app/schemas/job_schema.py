from marshmallow import Schema, fields


class JobSchema(Schema):
    id = fields.Int()
    name = fields.Str()
    icon = fields.Str()
