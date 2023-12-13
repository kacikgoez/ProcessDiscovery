from marshmallow import Schema, fields

from backend.src.flask.schemas.disaggregation_attribute_schema import DisaggregationAttributeSchema


class DistributionSchema(Schema):
    disaggregation_attribute = fields.Nested(DisaggregationAttributeSchema, required=True)
