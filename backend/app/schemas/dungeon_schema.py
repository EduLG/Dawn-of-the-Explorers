from marshmallow import Schema, fields


class DungeonSchema(Schema):
    id                = fields.Int()
    name              = fields.Str()
    description       = fields.Str()
    image_path        = fields.Str()
    min_rating        = fields.Int()
    visibility_rating = fields.Int()
    duration          = fields.Int()
