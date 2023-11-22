from marshmallow import Schema, fields
from marshmallow.validate import OneOf


class GetVariantListSchema(Schema):
    disaggregation_attribute = fields.Str(allow_none=True, validate=OneOf(['activity', 'resource', 'time']))
