import numpy as np
import pandas as pd

from backend.src.dataclasses.attributes import AttributeType, CategoricalAttribute, NumericalAttribute, \
    DisaggregationAttribute, PatientAttribute
from backend.src.dataclasses.filters import FilterOperator, BaseFilter
from definitions import PATIENT_ATTRIBUTES, FILTER_ATTRIBUTES


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

    # Calculate all filter attribute related columns
    process_attributes = df.groupby('case:concept:name').agg(
        start_activity=('concept:name', 'first'),
        end_activity=('concept:name', 'last'),
        case_size=('concept:name', 'count'),
        variant=('concept:name', lambda x: ' '.join(x)),
        case_duration=('time:timestamp', lambda x: (x.iloc[-1] - x.iloc[0]).seconds)
    )

    # Convert the categorical columns to categorical
    categorical_columns = [k for k, v in FILTER_ATTRIBUTES.items() if v == AttributeType.CATEGORICAL]
    process_attributes[categorical_columns] = process_attributes[categorical_columns].astype('category')

    # Convert the numerical columns to int as int64 cannot be serialized to JSON
    numerical_columns = [k for k, v in FILTER_ATTRIBUTES.items() if v == AttributeType.NUMERICAL]
    process_attributes[numerical_columns] = process_attributes[numerical_columns].astype(np.float64)

    # Merge the process attributes with the event log
    df = df.merge(process_attributes, on='case:concept:name')

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


def load_filter_attributes(event_log: pd.DataFrame) -> list[PatientAttribute]:
    """
    Load the filter attributes from the event log. For categorical attributes, all possible values will be extracted.
    For numerical attributes, the minimum and maximum value will be extracted.

    Args:
        event_log (pd.DataFrame): The event log.

    Returns:
        (list[PatientAttribute]): The filter attributes.
    """
    attributes = []

    # Iterate over all filter attributes and add them to the corresponding list
    for name, attribute_type in FILTER_ATTRIBUTES.items():
        if attribute_type == AttributeType.CATEGORICAL:
            attributes.append(CategoricalAttribute(name, event_log[name].cat.categories))
        elif attribute_type == AttributeType.NUMERICAL:
            attributes.append(NumericalAttribute(name, event_log[name].min(), event_log[name].max()))

    return attributes


def create_bins(el: pd.DataFrame, disaggregation_attribute: DisaggregationAttribute | None = None) \
        -> tuple[pd.DataFrame, str | None]:
    """
    Create bins for the given data frame. The bins will be created based on the given disaggregation attribute.
    If no disaggregation attribute or a categorical disaggregation attribute is given, the data frame will not be
    modified. If a numerical disaggregation attribute is given, the data frame will be binned based on the bins of the
    disaggregation attribute. The bins will be represented by the bin labels of the disaggregation attribute.

    Args:
        el (pd.DataFrame): The data frame.
        disaggregation_attribute (DisaggregationAttribute, optional): The disaggregation attribute. Defaults to None.

    Returns:
        (pd.DataFrame): The data frame.
        (str): The name of the column containing the disaggregation attribute.
    """
    # copy the column of the disaggregation attribute to a temporary column to avoid modifying the original data frame
    if disaggregation_attribute is not None:
        # copy the dataframe to avoid modifying the original data frame
        el = el.copy()

        if disaggregation_attribute.type == AttributeType.NUMERICAL:
            # bin the numerical values
            el[disaggregation_attribute.name] = pd.cut(el[disaggregation_attribute.name],
                                                       bins=disaggregation_attribute.get_bins(),
                                                       labels=disaggregation_attribute.get_bin_labels())

    return el, disaggregation_attribute.name if disaggregation_attribute is not None else None


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
