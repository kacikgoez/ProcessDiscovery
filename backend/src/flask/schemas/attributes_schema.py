from marshmallow import Schema, fields, ValidationError, validates_schema, post_load
from marshmallow.validate import OneOf, Length

from backend.src.dataclasses.attributes import AttributeType, DisaggregationAttribute
from definitions import PATIENT_ATTRIBUTES


class DisaggregationAttributeSchema(Schema):
    name = fields.Str(required=True,
                      validate=OneOf(PATIENT_ATTRIBUTES.keys()))
    bins = fields.List(fields.Int, allow_none=True, validate=Length(min=2))

    @validates_schema
    def validate_schema(self, data, **kwargs):
        attribute_type = PATIENT_ATTRIBUTES[data['name']]
        if attribute_type == AttributeType.NUMERICAL:
            if 'bins' not in data:
                raise ValidationError('The bins must be specified for numerical attributes.')

            bins = data['bins']
            # check if the bins are sorted
            for i in range(len(bins) - 1):
                if bins[i] >= bins[i + 1]:
                    raise ValidationError('The bins must be sorted in ascending order.')

        else:
            if 'bins' in data:
                raise ValidationError('The bins must not be specified for categorical attributes.')

    @post_load
    def make_disaggregation_attribute(self, data, **kwargs):
        attribute_type = PATIENT_ATTRIBUTES[data['name']]

        return DisaggregationAttribute(**data, type=attribute_type)
