from marshmallow import Schema, fields
from .party_schema import PartySchema


class UserSchema(Schema):
    id = fields.Str()
    username = fields.Str()
    email = fields.Str()
    party = fields.Nested(PartySchema, allow_none=True)
