import pandas as pd

from backend.src.dataclasses import PatientAttributes, CategoricalAttribute, AttributeType, NumericalAttribute
from definitions import PATIENT_ATTRIBUTES


def load_event_log(path: str) -> pd.DataFrame:
    """Load the event log from the given path.

    Args:
        path (str): The path to the event log.

    Returns:
        pd.DataFrame: The event log.
    """
    # Load the event log
    df = pd.read_csv(path, sep=',')

    # Convert the time columns to datetime
    df['time:timestamp'] = pd.to_datetime(df['time:timestamp'], format='ISO8601')

    # Convert the categorical columns to categorical
    categorical_columns = [k for k, v in PATIENT_ATTRIBUTES.items() if v == AttributeType.CATEGORICAL]
    df[categorical_columns] = df[categorical_columns].astype('category')

    return df


def load_patient_attributes(event_log: pd.DataFrame) -> PatientAttributes:
    """Load the patient attributes from the event log.

    Args:
        event_log (pd.DataFrame): The event log.

    Returns:
        PatientAttributes: The patient attributes.
    """
    categorical_attributes = []
    numerical_attributes = []

    # Iterate over all patient attributes and add them to the corresponding list
    for name, attribute_type in PATIENT_ATTRIBUTES.items():
        if attribute_type == AttributeType.CATEGORICAL:
            categorical_attributes.append(CategoricalAttribute(name, event_log[name].cat.categories))
        elif attribute_type == AttributeType.NUMERICAL:
            numerical_attributes.append(NumericalAttribute(name, event_log[name].min(), event_log[name].max())
                                        .create_groups(5))

    return PatientAttributes(categorical_attributes, numerical_attributes)
