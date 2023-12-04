from typing import Dict, List, Any
import pandas as pd
from pm4py.filtering import filter_variants, filter_between
from pm4py.statistics.end_activities.log.get import get_end_activities
from pm4py.stats import get_all_case_durations
from pm4py import discover_dfg


DE_JURE_VARIANT = ('Referral', 'Evaluation', 'Approach', 'Authorization', 'Procurement', 'Transplant')


def get_happy_path_adherence(el: pd.DataFrame, disaggregation_column: str, legend_column: str) -> Dict[str, List[Any]]:
    """
    :param legend_column:
    :param el: The event log
    :param disaggregation_column:
    :return: A dictionary contains key-value pairs of attribute's value and a list of happy path proportions,
            as well as key-value pair for legend and the x-axis values.
    """

    # get case number in each referral_year considering disaggregation_attribute
    year_case = el.groupby([disaggregation_column, legend_column]) \
        .apply(lambda x: x['case:concept:name'].nunique()) \
        .unstack()

    # filter only happy path
    variant = filter_variants(el,
                              [DE_JURE_VARIANT],
                              retain=True,
                              activity_key='concept:name',
                              case_id_key='case:concept:name',
                              timestamp_key='time:timestamp')

    # get number of happy path in each year considering disaggregation_attribute
    year_happy_proportion = variant.groupby([disaggregation_column, legend_column]) \
                                .apply(lambda x: x['case:concept:name'].nunique()).unstack() / year_case

    legend = year_happy_proportion.keys().tolist()

    result_dict = {}
    for index, row in year_happy_proportion.iterrows():
        result_dict[index] = row.tolist()

    result_dict.update({'legend': legend})

    return result_dict


def get_dropout_quantity(el: pd.DataFrame, disaggregation_attribute: str) -> Dict[str, List[Any]]:
    """
    :param el: The event log
    :param disaggregation_attribute:
    :return: A dictionary contains key-value pairs of attribute's value and a list of droppot quantity,
            as well as key-value pair for legend and the x-axis values.
    """

    # get the end actvitity of each case considering disaggregation_attribute
    drop_quantity = el.groupby(disaggregation_attribute).apply(lambda x: get_end_activities(x))

    legend = set()
    result_dict = {}
    for index, row in drop_quantity.items():
        legend.update(pd.json_normalize(row).keys().tolist())
        result_dict[index] = pd.json_normalize(row).values.ravel().tolist()

    legend = list(legend)
    result_dict.update({'legend': legend})

    return result_dict


def get_dropout_percentage(el: pd.DataFrame, disaggregation_attribute: str) -> Dict[str, List[Any]]:
    """
    :param el: The event log
    :param disaggregation_attribute:
    :return: A dictionary contains key-value pairs of attribute's value and a list of droppot percentage,
            as well as key-value pair for legend and the x-axis values.
    """

    # get case number
    total_case = el['case:concept:name'].nunique()

    # get the dropout percentage
    drop_quantity = get_dropout_quantity(el, disaggregation_attribute)

    # add percentage
    percentage = {}
    for key, value in drop_quantity.items():
        if key != 'legend':
            per = [x / total_case for x in value]
            percentage.update({key: per})
        else:
            percentage.update({key: value})
    return percentage


def get_permuted_path(el: pd.DataFrame, disaggregation_attribute: str) -> Dict[str, List[Any]]:
    """
    :param el: The event log
    :param disaggregation_attribute:
    :return: A dictionary contains key-value pairs of attribute's value and a list of permuted_path numbers,
            a key-value pair of  'case years' and a list of case numbers,
            and a key-value pair for legend and the x-axis values.
    """

    # Processing timestamp
    el['time:timestamp'] = pd.to_datetime(el['time:timestamp'], format='ISO8601')
    el = el.dropna(subset=['time:timestamp'])

    # filter out happy path
    variant = filter_variants(el,
                              [DE_JURE_VARIANT],
                              retain=False,
                              activity_key='concept:name',
                              case_id_key='case:concept:name',
                              timestamp_key='time:timestamp')

    # get number of happy path in each year considering disaggregation_attribute
    permuted_path = variant.groupby([disaggregation_attribute, 'referral_year']).apply(
        lambda x: x['case:concept:name'].nunique()).unstack()

    # get case number in each referral_year considering disaggregation_attribute
    year_case = el.groupby('referral_year').apply(lambda x: x['case:concept:name'].nunique()).tolist()

    legend = permuted_path.keys().tolist()

    result_dict = {}
    for index, row in permuted_path.iterrows():
        result_dict[index] = row.tolist()

    result_dict.update({'year cases': year_case})
    result_dict.update({'legend': legend})

    return result_dict


def get_permuted_path_dfg(el: pd.DataFrame) -> Dict[str, List[Dict[str, str | int]]]:
    """
    :param el:The event log
    :return: a dictionary composed of a list of dict containing nodes with activities and
             another list of dict containing directly-following relationships.
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
    :return: a pd.Series of list [refferal_year, bureaucratic_duration], indexed by disaggregation_attribute
    """

    # Processing timestamp
    el['time:timestamp'] = pd.to_datetime(el['time:timestamp'], format='ISO8601')
    el = el.dropna(subset=['time:timestamp'])

    # filter on only happy path
    variant = filter_between(el, 'Referral', 'Procurement',
                             activity_key='concept:name',
                             case_id_key='case:concept:name',
                             timestamp_key='time:timestamp')
    # case duration of happy path in each year considering disaggregation_attribute
    subcase_duration = variant.groupby([disaggregation_attribute,
                                        'referral_year']).apply(lambda x: get_all_case_durations(x))
    reshape = subcase_duration.explode().to_frame().reset_index().set_index(disaggregation_attribute)

    # conmbine the referral year and duration in minuten as a vector
    result = reshape.apply(lambda x: [x['referral_year'], x[0] / 60], axis=1)
    result = result.groupby(disaggregation_attribute).apply(list)

    return result


def get_evaluation_to_approach(el: pd.DataFrame, disaggregation_attribute: str) -> pd.Series:
    """
    :param el: The event log
    :param disaggregation_attribute:
    :return: a pd.Series of list [refferal_year, evaluation_to_approach_duration], indexed by disaggregation_attribute
    """

    # Processing timestamp
    el['time:timestamp'] = pd.to_datetime(el['time:timestamp'], format='ISO8601')
    el = el.dropna(subset=['time:timestamp'])

    # filter on only happy path
    variant = filter_between(el, 'Evaluation', 'Approach',
                             activity_key='concept:name',
                             case_id_key='case:concept:name',
                             timestamp_key='time:timestamp')
    # case duration of happy path in each year considering disaggregation_attribute
    subcase_duration = variant.groupby([disaggregation_attribute,
                                        'referral_year']).apply(lambda x: get_all_case_durations(x))
    reshape = subcase_duration.explode().to_frame().reset_index().set_index(disaggregation_attribute)

    # conmbine the referral year and duration in minuten as a vector
    result = reshape.apply(lambda x: [x['referral_year'], x[0] / 60], axis=1)
    result = result.groupby(disaggregation_attribute).apply(list)

    return result


def get_authorization_to_procurement(el: pd.DataFrame, disaggregation_attribute: str) -> pd.Series:
    """
    :param el: The event log
    :param disaggregation_attribute:
    :return: a pd.Series of list [refferal_year, authorization_to_procurement], indexed by disaggregation_attribute
    """

    # Processing timestamp
    el['time:timestamp'] = pd.to_datetime(el['time:timestamp'], format='ISO8601')
    el = el.dropna(subset=['time:timestamp'])

    # filter on only happy path
    variant = filter_between(el, 'Authorization', 'Procurement',
                             activity_key='concept:name',
                             case_id_key='case:concept:name',
                             timestamp_key='time:timestamp')
    # case duration of happy path in each year considering disaggregation_attribute
    subcase_duration = variant.groupby([disaggregation_attribute,
                                        'referral_year']).apply(lambda x: get_all_case_durations(x))
    reshape = subcase_duration.explode().to_frame().reset_index().set_index(disaggregation_attribute)

    # conmbine the referral year and duration in minuten as a vector
    result = reshape.apply(lambda x: [x['referral_year'], x[0] / 60], axis=1)
    result = result.groupby(disaggregation_attribute).apply(list)

    return result
