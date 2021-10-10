from marshmallow import Schema, fields


class LocationSchema(Schema):
    id = fields.Integer()
    person_id = fields.Integer()
    longitude = fields.String()
    latitude = fields.String()
    creation_time = fields.String()
