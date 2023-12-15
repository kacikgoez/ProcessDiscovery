from marshmallow import Schema, fields, post_load, ValidationError, validates_schema
from marshmallow.validate import OneOf

from backend.src.dataclasses.filters import NumericalFilter, CategoricalFilter, FilterOperator
from backend.src.dataclasses.attributes import AttributeType
from definitions import PATIENT_ATTRIBUTES

CATEGORICAL_ATTRIBUTES = [k for k, v in PATIENT_ATTRIBUTES.items() if v == AttributeType.CATEGORICAL]
NUMERICAL_ATTRIBUTES = [k for k, v in PATIENT_ATTRIBUTES.items() if v == AttributeType.NUMERICAL]


class CategoryFilterSchema(Schema):
    attribute_name = fields.Str(required=True, validate=OneOf(CATEGORICAL_ATTRIBUTES))
    operator = fields.Enum(FilterOperator, required=True, validate=OneOf(CategoricalFilter.supported_operators()))
    values = fields.List(fields.Str(), required=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data['operator'] in [FilterOperator.EQUALS, FilterOperator.NOT_EQUALS]:
            if len(data['values']) != 1:
                raise ValidationError('The operator requires a single value.')
        elif data['operator'] in [FilterOperator.CONTAINS, FilterOperator.NOT_CONTAINS]:
            if len(data['values']) == 0:
                raise ValidationError('The operator requires at least one value.')
        else:
            raise ValidationError('The operator is not supported for categorical attributes.')

    @post_load
    def make_filter(self, data, **kwargs):
        return CategoricalFilter(**data)


class NumericalFilterSchema(Schema):
    attribute_name = fields.Str(required=True, validate=OneOf(NUMERICAL_ATTRIBUTES))
    operator = fields.Enum(FilterOperator, required=True, validate=OneOf(NumericalFilter.supported_operators()))
    value = fields.Float(required=True)

    @post_load
    def make_filter(self, data, **kwargs):
        return NumericalFilter(**data)
