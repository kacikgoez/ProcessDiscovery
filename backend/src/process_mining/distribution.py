import pandas as pd
from typing import Dict, List


def attribute_distribution(el: pd.DataFrame, attribute: str) -> List[Dict[str, str | float]]:
    """
    Calculate the distribution of each value for a specified attribute in the event log. NaN values are represented
    by 'None' in the result.

    Args:
        el (pd.DataFrame): The event log DataFrame.
        attribute (str): The attribute in the event log for which the distribution is calculated.

    Returns:
        List[Dict[str, str | float]]: A list of dictionaries, each containing:
            - 'name': The value of the attribute.
            - 'value': The count of occurrences for the specified value, considering NaN.
    """

    # get first row of each case
    first_row = el.groupby('case:concept:name').first()
    # compute distribution considering nan
    column_distribution = first_row[attribute].value_counts(dropna=False)
    # rename nan in index to None
    column_distribution.index = column_distribution.index.map(lambda x: "None" if pd.isna(x) else x)

    column_distribution_list = [{'name': key, 'value': value} for key, value in
                                column_distribution.to_dict().items() if key is not None]

    return column_distribution_list
