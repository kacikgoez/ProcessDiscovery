import pandas as pd

from backend.src.dataclasses.attributes import AttributeType, CategoricalAttribute, NumericalAttribute, \
    DisaggregationAttribute, PatientAttribute
from backend.src.dataclasses.filters import FilterOperator, BaseFilter
from definitions import PATIENT_ATTRIBUTES


def load_event_log(path: str) -> pd.DataFrame:
    """
    Load the event log from the given path. The time column will be converted to datetime and the categorical columns
    will be converted to categorical.

    Args:
        path (str): The path to the event log.

    Returns:
        (pd.DataFrame): The event log.
    """
    # Load the event log
    df = pd.read_csv(path, sep=',')

    # Convert the time columns to datetime
    df['time:timestamp'] = pd.to_datetime(df['time:timestamp'], format='ISO8601')

    # Convert the categorical columns to categorical
    categorical_columns = [k for k, v in PATIENT_ATTRIBUTES.items() if v == AttributeType.CATEGORICAL]
    df[categorical_columns] = df[categorical_columns].astype('category')

    return df


def load_patient_attributes(event_log: pd.DataFrame) -> list[PatientAttribute]:
    """
    Load the patient attributes from the event log. For categorical attributes, all possible values will be extracted.
    For numerical attributes, the minimum and maximum value will be extracted.

    Args:
        event_log (pd.DataFrame): The event log.

    Returns:
        (list[PatientAttribute]): The patient attributes.
    """
    attributes = []

    # Iterate over all patient attributes and add them to the corresponding list
    for name, attribute_type in PATIENT_ATTRIBUTES.items():
        if attribute_type == AttributeType.CATEGORICAL:
            attributes.append(CategoricalAttribute(name, event_log[name].cat.categories))
        elif attribute_type == AttributeType.NUMERICAL:
            attributes.append(NumericalAttribute(name, event_log[name].min(), event_log[name].max()))

    return attributes


def create_bins(el: pd.DataFrame, disaggregation_attribute: DisaggregationAttribute | None = None,
                temporary_column_name='temp') -> pd.DataFrame:
    """
    Create bins for the given data frame. The bins will be created based on the given disaggregation attribute.
    If no disaggregation attribute or a categorical disaggregation attribute is given, the data frame will not be
    modified. If a numerical disaggregation attribute is given, the data frame will be modified by adding a temporary
    column containing the bin labels. The bin labels will be created based on the bins of the disaggregation attribute.

    Args:
        el (pd.DataFrame): The data frame.
        disaggregation_attribute (DisaggregationAttribute, optional): The disaggregation attribute. Defaults to None.
        temporary_column_name (str, optional): The name of the temporary column. Defaults to 'temp'.

    Returns:
        (pd.DataFrame): The data frame with the temporary column containing the bin labels.
    """
    # copy the column of the disaggregation attribute to a temporary column to avoid modifying the original data frame
    if disaggregation_attribute is not None:
        el[temporary_column_name] = el[disaggregation_attribute.name]

        if disaggregation_attribute.type == AttributeType.NUMERICAL:
            # bin the numerical values
            el[temporary_column_name] = pd.cut(el[temporary_column_name],
                                               bins=disaggregation_attribute.get_bins(),
                                               labels=disaggregation_attribute.get_bin_labels())

    return el


def filter_log(el: pd.DataFrame, filters: list[BaseFilter]) -> pd.DataFrame:
    """
    Filter the event log based on the given filters. The filters will be applied in the order they are given.
    As all filters are applied to the same data frame, one can think of the filters combined with a logical AND.

    Args:
        el (pd.DataFrame): The event log.
        filters (list[BaseFilter]): The filters.

    Returns:
        (pd.DataFrame): The filtered event log.
    """
    for filter in filters:
        match filter.operator:
            case FilterOperator.IS_EMPTY:
                el = el[el[filter.attribute_name].isna()]
            case FilterOperator.IS_NOT_EMPTY:
                el = el[el[filter.attribute_name].notna()]
            case FilterOperator.EQUALS:
                el = el[el[filter.attribute_name] == filter.filter_value]
            case FilterOperator.NOT_EQUALS:
                el = el[el[filter.attribute_name] != filter.filter_value]
            case FilterOperator.CONTAINS:
                el = el[el[filter.attribute_name].isin(filter.filter_value)]
            case FilterOperator.NOT_CONTAINS:
                el = el[~el[filter.attribute_name].isin(filter.filter_value)]
            case FilterOperator.LESS_THAN:
                el = el[el[filter.attribute_name] < filter.filter_value]
            case FilterOperator.LESS_THAN_OR_EQUALS:
                el = el[el[filter.attribute_name] <= filter.filter_value]
            case FilterOperator.GREATER_THAN:
                el = el[el[filter.attribute_name] > filter.filter_value]
            case FilterOperator.GREATER_THAN_OR_EQUALS:
                el = el[el[filter.attribute_name] >= filter.filter_value]
            case _:
                raise ValueError('The operator is not supported.')

    return el
