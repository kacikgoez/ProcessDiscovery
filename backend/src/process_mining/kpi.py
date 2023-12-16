from typing import Dict, List, Any
import pandas as pd
from pm4py.filtering import filter_variants, filter_between
from pm4py.statistics.end_activities.log.get import get_end_activities
from pm4py.stats import get_all_case_durations
from pm4py import discover_dfg


DE_JURE_VARIANT = ('Referral', 'Evaluation', 'Approach', 'Authorization', 'Procurement', 'Transplant')


def get_happy_path_adherence(el: pd.DataFrame, disaggregation_column: str, legend_column: str) -> Dict[str, List[Any]]:
    """
    Calculate happy path adherence proportions for different attributes in the event log.

    Args:
        el (pd.DataFrame): The event log DataFrame.
        disaggregation_column (str): The column used for disaggregation.
        legend_column (str): The column used for legend.

    Returns:
        Dict[str, List[Any]]: A dictionary containing:
            - 'legend': A list of legend values in the chart.
            - 'axis': A list of axis values in the chart.
            - 'value': A subdictionary with key-value pairs for happy path rate
              considering the specified disaggregation attribute.
    """

    # get case number in each legend_column value considering disaggregation_attribute
    legend_case = el.groupby([disaggregation_column, legend_column]) \
        .apply(lambda x: x['case:concept:name'].nunique()) \
        .unstack().fillna(0)

    # filter only happy path
    variant = filter_variants(el,
                              [DE_JURE_VARIANT],
                              retain=True,
                              activity_key='concept:name',
                              case_id_key='case:concept:name',
                              timestamp_key='time:timestamp')

    # get number of happy path in legend_column value considering disaggregation_attribute
    legend_happy_proportion = variant.groupby([disaggregation_column, legend_column]) \
                                .apply(lambda x: x['case:concept:name'].nunique()).unstack() / legend_case
    legend_happy_proportion_nan = legend_happy_proportion.fillna(0)

    axis = legend_happy_proportion.keys().tolist()
    legend = legend_happy_proportion.index.tolist()

    value = {}
    for index, row in legend_happy_proportion_nan.iterrows():
        value[index] = row.tolist()

    return {'legend': legend, 'axis': axis, 'value': value}


def get_dropout(el: pd.DataFrame, disaggregation_column: str) -> Dict[str, List[Any] | Dict[str, List[Any]]]:
    """
    Calculate dropout information based on a specified disaggregation attribute in the event log.

    Args:
        el (pd.DataFrame): The event log.
        disaggregation_column (str): The column used for disaggregation.

    Returns:
        Dict[str, List[Any] | Dict[str, List[Any]]]: A dictionary containing:
            - 'legend': A key-value pair of legend in the chart and its value.
            - 'axis': A key-value pair of axis in the chart and its value.
            - 'value': A subdictionary with key-value pairs for dropout quality and dropout percentage
              considering the specified disaggregation attribute.
    """

    # get the end actvitity of each case considering disaggregation_attribute
    drop_quantity = el.groupby(disaggregation_column).apply(lambda x: get_end_activities(x))
    # drop nan in result
    drop_quantity_nan = pd.DataFrame(drop_quantity.tolist(), index=drop_quantity.index).fillna(0)
    # get case number
    total_case = el['case:concept:name'].nunique()

    axis = drop_quantity_nan.keys().tolist()

    value = {}
    for index, row in drop_quantity_nan.iterrows():
        value[index] = row.tolist()
        value[index + '_percentage'] = [x / total_case if total_case != 0 else 0 for x in row.tolist()]
    legend = list(value.keys())

    return {'legend': legend, 'axis': axis, 'value': value}


def get_permuted_path(el: pd.DataFrame, disaggregation_column: str, legend_column: str) -> Dict[str, List[Any] |
                                                                                                Dict[str, List[Any]]]:
    """
    Calculate permuted path information based on specified disaggregation attributes in the event log.

    Args:
        el (pd.DataFrame): The event log.
        disaggregation_column (str): The column used for disaggregation.
        legend_column (str): The column used for legend.

    Returns:
        Dict[str, List[Any] | Dict[str, List[Any]]]: A dictionary containing:
            - 'legend': A key-value pair of legend in the chart and its value.
            - 'axis': A key-value pair of axis in the chart and its value.
            - 'value': A subdictionary with key-value pairs for permuted path number
              considering the specified disaggregation attributes and year case number.
    """

    # filter out happy path
    variant = filter_variants(el,
                              [DE_JURE_VARIANT],
                              retain=False,
                              activity_key='concept:name',
                              case_id_key='case:concept:name',
                              timestamp_key='time:timestamp')

    # get number of happy path in each year considering disaggregation_attribute
    permuted_path = variant.groupby([disaggregation_column, legend_column]).apply(
        lambda x: x['case:concept:name'].nunique()).unstack()

    # get case number in each legend value considering disaggregation_attribute
    legend_case = el.groupby(legend_column).apply(lambda x: x['case:concept:name'].nunique()).tolist()

    axis = permuted_path.keys().tolist()

    value = {'total_cases': legend_case}
    for index, row in permuted_path.iterrows():
        value[index] = row.fillna(0).tolist()

    legend = list(value.keys())

    return {'legend': legend, 'axis': axis, 'value': value}


def get_permuted_path_dfg(el: pd.DataFrame) -> Dict[str, List[Dict[str, str | int]]]:
    """
    Generate a Process Mining DFG based on the given event log.

    Args:
        el (pd.DataFrame): The event log.

    Returns:
        Dict[str, List[Dict[str, str | int]]]: A dictionary containing:
            - 'nodes': A list of dictionaries representing nodes with activities.
            - 'links': A list of dictionaries representing directly-following relationships.
    """

    # find the directly-following graph
    dfg, start_activities, end_activities = discover_dfg(el, case_id_key='case:concept:name',
                                                        activity_key='concept:name', timestamp_key='time:timestamp')

    act = set()
    links = []

    for pair, freq in dfg.items():
        # find directly-following relations
        links.append(
            {
                'source': pair[0],
                'target': pair[1],
                'absolute_frequency': freq
            }
        )
        # find activities in the log
        act.update([pair[0], pair[1]])

    nodes = []
    for value in act:
        nodes.append(
            {
                'name': value
            }
        )

    return {'nodes': nodes, 'links': links}


def get_bureaucratic_duration(el: pd.DataFrame, disaggregation_column: str, legend_column: str) -> Dict[str, List[Any] |
                                                                                                Dict[str, List[Any]]]:
    """
    Calculate bureaucratic duration based on specified disaggregation attributes in the event log.

    Args:
        el (pd.DataFrame): The event log.
        disaggregation_column (str): The column used for disaggregation.
        legend_column (str): The column used for legend.

    Returns:
        Dict[str, List[Any] | Dict[str, List[Any]]]: A dictionary containing:
            - 'legend': A key-value pair of legend in the chart and its value.
            - 'value': A subdictionary with key-value pairs for a list of vectors [referral_year,
              referral_to_procurement_duration] considering the specified disaggregation attributes.
    """

    # filter on only happy path
    variant = filter_between(el, 'Referral', 'Procurement',
                              activity_key='concept:name',
                              case_id_key='case:concept:name',
                              timestamp_key='time:timestamp')
    # case duration of happy path in each legend value considering disaggregation_attribute
    subcase_duration = variant.groupby([disaggregation_column, legend_column]).apply(lambda x: get_all_case_durations(x))
    reshape = subcase_duration.explode().to_frame().reset_index().set_index(disaggregation_column)

    # conmbine the legend value and duration in minuten as a vector
    result = reshape.apply(lambda x: [x[legend_column], round(x[0]/60)], axis=1)
    result = result.groupby(disaggregation_column).apply(list).to_dict()

    legend = list(result.keys())

    return {'legend': legend, 'value': result}


def get_evaluation_to_approach(el: pd.DataFrame, disaggregation_column: str, legend_column: str) -> Dict[str, List[Any] |
                                                                                        Dict[str, List[Any]]]:
    """
        Calculate evaluation-to-approach duration information based on specified disaggregation attributes in the
        event log.

        Args:
            el (pd.DataFrame): The event log.
            disaggregation_column (str): The column used for disaggregation.
            legend_column (str): The column used for legend.

        Returns:
            Dict[str, List[Any] | Dict[str, List[Any]]]: A dictionary containing:
                - 'legend': A key-value pair of legend in the chart and its value.
                - 'value': A subdictionary with key-value pairs for a list of vectors
                [legend value, evaluation_to_approach_duration] considering the specified disaggregation attributes.
        """

    # Processing timestamp
    el['time:timestamp'] = pd.to_datetime(el['time:timestamp'], format='ISO8601')
    el = el.dropna(subset=['time:timestamp'])

    # filter on only happy path
    variant = filter_between(el, 'Evaluation', 'Approach',
                              activity_key='concept:name',
                              case_id_key='case:concept:name',
                              timestamp_key='time:timestamp')
    # case duration of happy path in legend value considering disaggregation_attribute
    subcase_duration = variant.groupby([disaggregation_column, legend_column]).apply(
        lambda x: get_all_case_durations(x))
    reshape = subcase_duration.explode().to_frame().reset_index().set_index(disaggregation_column)

    # conmbine the legend value and duration in minuten as a vector
    result = reshape.apply(lambda x: [x[legend_column], round(x[0] / 60)], axis=1)
    result = result.groupby(disaggregation_column).apply(list).to_dict()

    legend = list(result.keys())

    return {'legend': legend, 'value': result}


def get_authorization_to_procurement(el: pd.DataFrame, disaggregation_column: str, legend_column: str) -> Dict[str,
                                                                                   List[Any] | Dict[str, List[Any]]]:
    """
        Calculate authorization-to-procurement duration information based on specified disaggregation attributes in
        the event log.

        Args:
            el (pd.DataFrame): The event log.
            disaggregation_column (str): The column used for disaggregation.
            legend_column (str): The column used for legend.

        Returns:
            Dict[str, List[Any] | Dict[str, List[Any]]]: A dictionary containing:
                - 'legend': A key-value pair of legend in the chart and its value.
                - 'value': A subdictionary with key-value pairs for a list of vectors
                 [legend value, authorization_to_procurement_duration] considering the specified
                 disaggregation attributes.
        """

    # filter on only happy path
    variant = filter_between(el, 'Authorization', 'Procurement',
                             activity_key='concept:name',
                             case_id_key='case:concept:name',
                             timestamp_key='time:timestamp')
    # case duration of happy path in each legend value considering disaggregation_attribute
    subcase_duration = variant.groupby([disaggregation_column, legend_column]).apply(
        lambda x: get_all_case_durations(x))
    reshape = subcase_duration.explode().to_frame().reset_index().set_index(disaggregation_column)

    # conmbine the legend value and duration in minuten as a vector
    result = reshape.apply(lambda x: [x[legend_column], round(x[0] / 60)], axis=1)
    result = result.groupby(disaggregation_column).apply(list).to_dict()

    legend = list(result.keys())
    return {'legend': legend, 'value': result}
