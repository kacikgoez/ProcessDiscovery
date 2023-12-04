import pandas as pd

from backend.src.dataclasses import DisaggregationAttribute, AttributeType


def create_bins(el: pd.DataFrame, disaggregation_attribute: DisaggregationAttribute, temporary_column_name='temp') -> \
        pd.DataFrame:
    # copy the column of the disaggregation attribute to a temporary column to avoid modifying the original data frame
    el[temporary_column_name] = el[disaggregation_attribute.name]

    # bin the numerical values
    if disaggregation_attribute.type == AttributeType.NUMERICAL:
        el[temporary_column_name] = pd.cut(el[temporary_column_name],
                                           bins=disaggregation_attribute.get_bins(),
                                           labels=disaggregation_attribute.get_bin_labels())

    return el
