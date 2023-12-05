from marshmallow import Schema, fields, ValidationError, validates_schema, post_load

from backend.src.dataclasses import KpiRequest, KpiType
from backend.src.flask.schemas.disaggregation_attribute_schema import DisaggregationAttributeSchema


class KpiSchema(Schema):
    kpi = fields.Enum(required=True, enum=KpiType)
    legend_attribute = fields.Nested(DisaggregationAttributeSchema, required=False)
    disaggregation_attribute = fields.Nested(DisaggregationAttributeSchema, required=False)

    @validates_schema
    def ensure_different_attributes(self, data, **kwargs):
        if 'legend_attribute' in data and data['legend_attribute'].name == data['disaggregation_attribute'].name:
            raise ValidationError('The legend attribute and the disaggregation attribute must be different.')

    @post_load
    def make_kpi_request(self, data, **kwargs):
        return KpiRequest(**data)
