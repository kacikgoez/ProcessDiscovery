from typing import Collection

import pandas as pd
from pm4py.objects.log.util import pandas_numpy_variants

from backend.src.dataclasses.charts import Variant


def get_variants_with_case_ids(el: pd.DataFrame) -> dict[Collection[str], list[str]]:
    """
    Returns a dictionary of variants (tuples of activity names) and the case ids that belong to them.

    Attributes:
        el (pd.DataFrame): The event log.

    Returns:
        A dictionary of variants and the case ids that belong to them.
    """
    # apply the pm4py function to get the variant per case
    _, cases = pandas_numpy_variants.apply(el, parameters={})

    # switch keys and values in the dictionary to get the list of cases per variant
    variants = {}
    for case_id, variant in cases.items():
        if variant not in variants:
            variants[variant] = []
        variants[variant].append(case_id)

    return variants


def get_variants_with_frequencies(el: pd.DataFrame, disaggregation_column: str) -> list[Variant]:
    """
    Returns a list of variants with their frequencies and distributions of the given disaggregation attribute.
    The variants are sorted by their frequency in descending order.

    Attributes:
        el (pd.DataFrame): The event log.
        disaggregation_column (str): The name of the column to disaggregate the variants.

    Returns:
        A list of variants with their frequencies and distributions of the given disaggregation attribute.
    """
    variants = get_variants_with_case_ids(el)
    total_case_count = el['case:concept:name'].nunique()

    result: list[Variant] = []
    for variant, case_ids in variants.items():
        distribution = el.loc[el['case:concept:name'].isin(case_ids)] \
            .groupby('case:concept:name') \
            .first()[disaggregation_column] \
            .value_counts(dropna=False)
        distribution.index = distribution.index.fillna('None')

        result.append(Variant(
            activities=list(variant),
            count=len(case_ids),
            frequency=len(case_ids) / total_case_count,
            distribution=distribution.to_dict(),
        ))

    # sort the variants by their frequency
    result.sort(key=lambda v: v.frequency, reverse=True)

    return result
