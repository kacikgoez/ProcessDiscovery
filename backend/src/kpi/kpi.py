from typing import Dict, List
import pandas as pd
import pm4py
from pm4py.filtering import filter_variants
from pm4py.statistics.end_activities.log.get import get_end_activities
from pm4py.stats import get_all_case_durations
from pm4py import discover_dfg


def get_happy_path_adherence(el: pd.DataFrame, disaggregation_attribute: str) -> pd.Series:
    """
    :param el: The event log
    :param disaggregation_attribute:
    :return: a pd.Series of the proportion of happy path, indexed by disaggregation_attribute
    """

    # Processing timestamp
    el['time:timestamp'] = pd.to_datetime(el['time:timestamp'], format='ISO8601')
    el = el.dropna(subset=['time:timestamp'])

    # get case number in each referral_year considering disaggregation_attribute
    year_case = el.groupby([disaggregation_attribute,
                            'referral_year']).apply(lambda x: x['case:concept:name'].nunique()).unstack()

    # filter only happy path
    variant = filter_variants(el,
                              [('Referral', 'Evaluation', 'Approach', 'Authorization', 'Procurement', 'Transplant')],
                              retain=True,
                              activity_key='concept:name',
                              case_id_key='case:concept:name',
                              timestamp_key='time:timestamp')

    # get number of happy path in each year considering disaggregation_attribute
    year_happy_proportion = variant.groupby([disaggregation_attribute, 'referral_year']).apply(
        lambda x: x['case:concept:name'].nunique()).unstack() / year_case

    return year_happy_proportion


def get_dropout_quantity(el: pd.DataFrame, disaggregation_attribute: str) -> pd.Series:
    """
    :param el: The event log
    :param disaggregation_attribute:
    :return: a pd.Series of dropout quantity, indexed by disaggregation_attribute
    """

    # get the end actvitity of each case considering disaggregation_attribute
    drop_quantity = el.groupby(disaggregation_attribute).apply(lambda x: get_end_activities(x))

    # convert to a series
    drop_quantity = drop_quantity.apply(pd.Series)

    return drop_quantity


def get_dropout_percentage(el: pd.DataFrame, disaggregation_attribute: str) -> pd.Series:
    """
    :param el: The event log
    :param disaggregation_attribute:
    :return: a pd.Series of dropout percenatge, indexed by disaggregation_attribute
    """

    # get the dropout quantity
    drop_quantity = get_dropout_quantity(el, disaggregation_attribute)
    # get case number
    total_case = el['case:concept:name'].nunique()
    # compute percentage of total cases (some disaggregation_attributes have nan-value, for example 122 nan in gender)
    dropout_percentage = drop_quantity / total_case

    return dropout_percentage


def get_permuted_path(el: pd.DataFrame) -> Dict[str, List[Dict[str, str | int]]]:
    """
    :param el:The event log
    :return: a dictionary composed of a list of dict containing nodes with activities and
             another list of dict containing irectly-following relationships.
    """

    # Processing timestamp
    el['time:timestamp'] = pd.to_datetime(el['time:timestamp'], format='ISO8601')
    el = el.dropna(subset=['time:timestamp'])

    # find the directly-following graph
    dfg, start_activities, end_activities = discover_dfg(el, case_id_key='case:concept:name',
                                                               activity_key='concept:name',
                                                               timestamp_key='time:timestamp')

    # find activities in the log
    act = set(start_activities.keys()).union(end_activities.keys())
    nodes = []
    for value in act:
        nodes.append(
            {
                'name': value

            }
        )
    # find directly-following relations
    links = []
    for pair, freq in dfg.items():
        links.append(
            {
                'source': pair[0],
                'target': pair[1],
                'absolute_frequency': freq

            }
        )

    return {'nodes': nodes, 'links': links}


def get_bureaucratic_duration(el: pd.DataFrame, disaggregation_attribute: str) -> pd.Series:
    """
    :param el: The event log
    :param disaggregation_attribute:
    :return: a pd.Series of list [refferal_year, case_duration], indexed by disaggregation_attribute
    """

    # Processing timestamp
    el['time:timestamp'] = pd.to_datetime(el['time:timestamp'], format='ISO8601')
    el = el.dropna(subset=['time:timestamp'])

    # filter on only happy path
    variant = filter_variants(el,
                              [('Referral', 'Evaluation', 'Approach', 'Authorization', 'Procurement', 'Transplant')],
                              retain=True,
                              activity_key='concept:name',
                              case_id_key='case:concept:name',
                              timestamp_key='time:timestamp')
    # case duration of happy path in each year considering disaggregation_attribute
    happy_duration = variant.groupby([disaggregation_attribute,
                                      'referral_year']).apply(lambda x:  get_all_case_durations(x))
    reshape = happy_duration.explode().to_frame().reset_index().set_index(disaggregation_attribute)

    # conmbine the referral year and duration in minuten as a vector
    result = reshape.apply(lambda x: [x['referral_year'], x[0]/60], axis=1)
    result = result.groupby(disaggregation_attribute).apply(list)

    return result


