from marshmallow import Schema, fields, validates_schema, post_load, ValidationError, pre_load

from backend.src.dataclasses.requests import VariantListRequest, KpiRequest, KpiType, DistributionRequest, DfgRequest
from backend.src.flask.schemas.attributes_schema import DisaggregationAttributeSchema
from backend.src.flask.schemas.filter_schemas import CategoryFilterSchema, NumericalFilterSchema


class FilteredRequestSchema(Schema):
    categorical_filters = fields.List(fields.Nested(CategoryFilterSchema), required=False)
    numerical_filters = fields.List(fields.Nested(NumericalFilterSchema), required=False)

    @post_load()
    def combine_filters(self, data, **kwargs):
        data['filters'] = []
        if 'categorical_filters' in data:
            data['filters'] += data['categorical_filters']
            del data['categorical_filters']
        if 'numerical_filters' in data:
            data['filters'] += data['numerical_filters']
            del data['numerical_filters']

        return data


class GetVariantListSchema(FilteredRequestSchema):
    disaggregation_attribute = fields.Nested(DisaggregationAttributeSchema, required=True)

    @post_load
    def make_variant_list_request(self, data, **kwargs):
        return VariantListRequest(**data)


class KpiSchema(FilteredRequestSchema):
    kpi = fields.Enum(required=True, enum=KpiType)
    legend_attribute = fields.Nested(DisaggregationAttributeSchema, required=False)
    disaggregation_attribute = fields.Nested(DisaggregationAttributeSchema, required=True)

    @validates_schema
    def ensure_different_attributes(self, data, **kwargs):
        if 'legend_attribute' in data and data['legend_attribute'].name == data['disaggregation_attribute'].name:
            raise ValidationError('The legend attribute and the disaggregation attribute must be different.')

    @post_load
    def make_kpi_request(self, data, **kwargs):
        return KpiRequest(**data)


class DistributionSchema(FilteredRequestSchema):
    disaggregation_attribute = fields.Nested(DisaggregationAttributeSchema, required=True)

    @post_load
    def make_distribution_request(self, data, **kwargs):
        return DistributionRequest(**data)


class DfgSchema(FilteredRequestSchema):
    disaggregation_attribute = fields.Nested(DisaggregationAttributeSchema, required=True)

    @post_load
    def make_dfg_request(self, data, **kwargs):
        return DfgRequest(**data)

