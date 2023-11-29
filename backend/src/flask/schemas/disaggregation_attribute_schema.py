from marshmallow import Schema, fields, ValidationError, validates_schema
from marshmallow.validate import OneOf, Length

from backend.src.dataclasses import AttributeType
from definitions import PATIENT_ATTRIBUTES


class IntervalSchema(Schema):
    lower = fields.Float(required=True)
    upper = fields.Float(required=True)

    @validates_schema
    def validate_schema(self, data, **kwargs):
        if data['lower'] >= data['upper']:
            raise ValidationError('The lower bound must be smaller than the upper bound.')


class DisaggregationAttributeSchema(Schema):
    name = fields.Str(required=True,
                      validate=OneOf(PATIENT_ATTRIBUTES.keys()))
    groups = fields.List(fields.Nested(IntervalSchema), allow_none=True, validate=Length(min=1))

    @validates_schema
    def validate_schema(self, data, **kwargs):
        attribute_type = PATIENT_ATTRIBUTES[data['name']]
        if attribute_type == AttributeType.NUMERICAL:
            if 'groups' not in data:
                raise ValidationError('The groups must be specified for numerical attributes.')

            groups = data['groups']
            for i in range(len(groups) - 1):
                if groups[i]['upper'] != groups[i + 1]['lower']:
                    raise ValidationError('The intervals must not have gaps between them.')

        else:
            if 'groups' in data:
                raise ValidationError('The groups must not be specified for categorical attributes.')