import pandas as pd

from backend.src.dataclasses.charts import DataSeries


def attribute_distribution(el: pd.DataFrame, attribute: str) -> DataSeries:
    """
    Calculate the distribution of each value for a specified attribute in the event log. NaN values are represented
    by 'None' in the result.

    Args:
        el (pd.DataFrame): The event log DataFrame.
        attribute (str): The attribute in the event log for which the distribution is calculated.

    Returns:
        DataSeries: The distribution of the attribute.
    """

    # get first row of each case
    first_row = el.groupby('case:concept:name').first()
    # compute distribution considering nan
    column_distribution = first_row[attribute].value_counts(dropna=False)
    # rename nan in index to None
    column_distribution.index = column_distribution.index.map(lambda x: "None" if pd.isna(x) else x)

    return DataSeries.from_dict(
        name=attribute,
        data=column_distribution.to_dict(),
        sort_by=attribute
    )
