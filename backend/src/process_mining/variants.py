from typing import Collection

import pandas as pd
from pm4py.objects.log.util import pandas_numpy_variants

from backend.src.dataclasses import Variant


def get_variants_with_case_ids(el: pd.DataFrame) -> dict[Collection[str], list[str]]:
    """
    Returns a dictionary of variants and the case ids that belong to them.
    The variants are tuples of activity names.

    :param el: The event log
    :return:
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

    :return:
    """
    variants = get_variants_with_case_ids(el)
    total_case_count = el['case:concept:name'].nunique()

    result: list[Variant] = []
    for variant, case_ids in variants.items():
        distribution = el.loc[el['case:concept:name'].isin(case_ids)] \
            .groupby('case:concept:name') \
            .first()[disaggregation_column] \
            .value_counts()

        result.append(Variant(
            activities=list(variant),
            count=len(case_ids),
            frequency=len(case_ids) / total_case_count,
            distribution=distribution.to_dict(),
        ))

    # sort the variants by their frequency
    result.sort(key=lambda v: v.frequency, reverse=True)

    return result
