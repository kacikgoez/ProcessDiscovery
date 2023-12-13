from marshmallow import Schema, fields, post_load
from backend.src.flask.schemas.disaggregation_attribute_schema import DisaggregationAttributeSchema
from backend.src.dataclasses import Filter


class FilterSchema(Schema):
    filter_attribute = fields.Nested(DisaggregationAttributeSchema, required=True)
    filter_values = fields.List(fields.String(), required=True)

    @post_load
    def make_filter_request(self, data, **kwargs):
        return Filter(**data)
