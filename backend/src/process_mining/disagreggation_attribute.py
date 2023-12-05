import pandas as pd

from backend.src.dataclasses import DisaggregationAttribute, AttributeType


def create_bins(el: pd.DataFrame, disaggregation_attribute: DisaggregationAttribute | None = None, temporary_column_name='temp') -> \
        pd.DataFrame:

    # copy the column of the disaggregation attribute to a temporary column to avoid modifying the original data frame
    if disaggregation_attribute is not None:
        el[temporary_column_name] = el[disaggregation_attribute.name]

        if  disaggregation_attribute.type == AttributeType.NUMERICAL:
             # bin the numerical values
            el[temporary_column_name] = pd.cut(el[temporary_column_name],
                                           bins=disaggregation_attribute.get_bins(),
                                           labels=disaggregation_attribute.get_bin_labels())

    return el

