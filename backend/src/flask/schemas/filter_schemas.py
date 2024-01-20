from marshmallow import Schema, fields, post_load, ValidationError, validates_schema
from marshmallow.validate import OneOf

from backend.src.dataclasses.filters import NumericalFilter, CategoricalFilter, FilterOperator
from backend.src.dataclasses.attributes import AttributeType
from definitions import PATIENT_ATTRIBUTES, FILTER_ATTRIBUTES

CATEGORICAL_ATTRIBUTES = [k for k, v in PATIENT_ATTRIBUTES.items() if v == AttributeType.CATEGORICAL]
CATEGORICAL_ATTRIBUTES += [k for k, v in FILTER_ATTRIBUTES.items() if v == AttributeType.CATEGORICAL]
NUMERICAL_ATTRIBUTES = [k for k, v in PATIENT_ATTRIBUTES.items() if v == AttributeType.NUMERICAL]
NUMERICAL_ATTRIBUTES += [k for k, v in FILTER_ATTRIBUTES.items() if v == AttributeType.NUMERICAL]


def validate_operator_value_count(operator: FilterOperator, values: list[any] | None):
    if operator.accepts_no_value:
        if values is not None:
            raise ValidationError('The operator does not accept a value.')
    elif operator.accepts_single_value:
        if values is None or len(values) != 1:
            raise ValidationError('The operator requires a single value.')
    elif operator.accepts_multiple_values:
        if values is None or len(values) == 0:
            raise ValidationError('The operator requires at least one value.')
    else:
        raise ValueError('The operator is not supported.')


class CategoryFilterSchema(Schema):
    attribute_name = fields.Str(required=True, validate=OneOf(CATEGORICAL_ATTRIBUTES))
    operator = fields.Enum(FilterOperator, required=True, validate=OneOf(CategoricalFilter.supported_operators()))
    values = fields.List(fields.Str(), required=True, allow_none=True)

    @validates_schema
    def validate_operator_value_count(self, data, **kwargs):
        validate_operator_value_count(data['operator'], data.get('values'))

    @post_load
    def make_filter(self, data, **kwargs):
        return CategoricalFilter(**data)


class NumericalFilterSchema(Schema):
    attribute_name = fields.Str(required=True, validate=OneOf(NUMERICAL_ATTRIBUTES))
    operator = fields.Enum(FilterOperator, required=True, validate=OneOf(NumericalFilter.supported_operators()))
    value = fields.Float(required=True, allow_none=True)

    @validates_schema
    def validate_operator_value_count(self, data, **kwargs):
        value = [data.get('value')] if data.get('value') is not None else None
        validate_operator_value_count(data['operator'], value)

    @post_load
    def make_filter(self, data, **kwargs):
        return NumericalFilter(**data)
