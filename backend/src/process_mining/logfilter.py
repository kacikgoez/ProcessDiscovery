import pandas as pd
from definitions import PATIENT_ATTRIBUTES


def filter_attribute(el: pd.DataFrame, filter_column: str, filter_values: list[str]) -> pd.DataFrame:
    """
    Args:
        el: The event log
        filter_column: Filtered attribute
        filter_values: Filtered value

    Returns: The datafram that filter_column only has filter_value

    """
    for name, attribute_type in PATIENT_ATTRIBUTES.items():
        # ensure the filter value in PATIENT_ATTRIBUTES
        if name == filter_column:
            el = el[el[filter_column + 'copy'].isin(filter_values)]
            if attribute_type == 'categorical':
                # remove the filtered out categorical values
                el[filter_column] = el[filter_column].cat.remove_unused_categories()

            # stop the loop
            break

    filtered_el = el.drop(columns=[filter_column + 'copy'])

    return filtered_el
