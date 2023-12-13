import pandas as pd
from typing import Dict, List, Any


def attribute_distribution(el: pd.DataFrame, attribute: str) -> Dict[str, List[Any]]:
    """
    Args:
        el: The event log
        attribute: the attribute in event log

    Returns: the distribution of attribute values

    """
    # get first row of each case
    first_row = el.groupby('case:concept:name').first()
    # compute distribution considering nan
    column_distribution = first_row[attribute].value_counts(normalize=True, dropna=False) * 100
    # rename nan in index to None
    column_distribution.index = column_distribution.index.map(lambda x: "None" if pd.isna(x) else x)

    return {"legend": column_distribution.index.to_list(), "value":column_distribution.to_list()}
