import pandas as pd
from pm4py.filtering import filter_variants, filter_between
from pm4py.stats import get_all_case_durations

from backend.src.dataclasses.charts import MultiDataSeries

DE_JURE_VARIANT = ('Referral', 'Evaluation', 'Approach', 'Authorization', 'Procurement', 'Transplant')


def get_happy_path_adherence(el: pd.DataFrame, disaggregation_column: str,
                             legend_column: str | None) -> MultiDataSeries:
    """
    Calculate happy path adherence proportions for different attributes in the event log.

    Args:
        el (pd.DataFrame): The event log DataFrame.
        disaggregation_column (str): The column used for disaggregation.
        legend_column (str | None): The column used for legend.

    Returns:
        The happy path adherence proportions for different attributes in the event log.
    """
    group = [disaggregation_column] if legend_column is None else [legend_column, disaggregation_column]

    # count the number of cases for each group
    legend_case = el.groupby(group) \
        .apply(lambda x: x['case:concept:name'].nunique()) \
        .fillna(0)

    # filter only happy path
    variant = filter_variants(el, [DE_JURE_VARIANT], retain=True)

    # count the number of happy paths for each group and divide by the number of cases in each group
    legend_happy_proportion = variant.groupby(group) \
                                  .apply(lambda x: x['case:concept:name'].nunique()) / legend_case
    legend_happy_proportion = legend_happy_proportion.fillna(0)

    return MultiDataSeries.from_pandas(legend_happy_proportion, 'Happy path adherence')


def get_dropout(el: pd.DataFrame, disaggregation_column: str) -> MultiDataSeries:
    """
    Calculate dropout information based on a specified disaggregation attribute in the event log.

    Args:
        el (pd.DataFrame): The event log.
        disaggregation_column (str): The column used for disaggregation.

    Returns:
        The dropout information based on a specified disaggregation attribute in the event log.
    """
    # We start by selecting the last activity and the corresponding disaggregation attribute for each case
    last_activities = el.groupby(by=['case:concept:name']).last()[[disaggregation_column, 'concept:name']]
    # We then count the number of cases for each last activity and disaggregation attribute
    last_activities_count = last_activities.value_counts()

    return MultiDataSeries.from_pandas(last_activities_count, 'Dropout rate')


def get_permuted_path(el: pd.DataFrame, disaggregation_column: str, legend_column: str | None) -> MultiDataSeries:
    """
    Calculate permuted path information based on specified disaggregation attributes in the event log.

    Args:
        el (pd.DataFrame): The event log.
        disaggregation_column (str): The column used for disaggregation.
        legend_column (str): The column used for legend.

    Returns:
        The permuted path information based on specified disaggregation attributes in the event log.
    """
    group = [disaggregation_column] if legend_column is None else [legend_column, disaggregation_column]

    # filter out happy path
    permuted_paths = filter_variants(el, [DE_JURE_VARIANT], retain=False)

    # count the number of cases for each group
    permuted_paths_count = permuted_paths.groupby(by=group) \
        .apply(lambda x: x['case:concept:name'].nunique()) \
        .fillna(0)

    return MultiDataSeries.from_pandas(permuted_paths_count, 'Permuted path adherence')


def get_bureaucratic_duration(el: pd.DataFrame, disaggregation_column: str, legend_column: str) -> MultiDataSeries:
    """
    Calculate bureaucratic duration based on specified disaggregation attributes in the event log.

    Args:
        el (pd.DataFrame): The event log.
        disaggregation_column (str): The column used for disaggregation.
        legend_column (str): The column used for legend.

    Returns:
        A data series containing the mean duration between referral and procurement for each group.
    """
    group = [disaggregation_column] if legend_column is None else [legend_column, disaggregation_column]

    subcase_duration = _get_duration_between_activities(el, 'Referral', 'Procurement', group)

    return MultiDataSeries.from_pandas(subcase_duration, 'Bureaucratic duration')


def get_evaluation_to_approach(el: pd.DataFrame, disaggregation_column: str, legend_column: str) -> MultiDataSeries:
    """
        Calculate evaluation-to-approach duration information based on specified disaggregation attributes in the
        event log.

        Args:
            el (pd.DataFrame): The event log.
            disaggregation_column (str): The column used for disaggregation.
            legend_column (str): The column used for legend.

        Returns:
            A data series containing the mean duration between evaluation and approach for each group.
        """
    group = [disaggregation_column] if legend_column is None else [legend_column, disaggregation_column]

    subcase_duration = _get_duration_between_activities(el, 'Evaluation', 'Approach', group)

    return MultiDataSeries.from_pandas(subcase_duration, 'Evaluation to approach')


def get_authorization_to_procurement(el: pd.DataFrame, disaggregation_column: str,
                                     legend_column: str) -> MultiDataSeries:
    """
        Calculate authorization-to-procurement duration information based on specified disaggregation attributes in
        the event log.

        Args:
            el (pd.DataFrame): The event log.
            disaggregation_column (str): The column used for disaggregation.
            legend_column (str): The column used for legend.

        Returns:
            A data series containing the mean duration between authorization and procurement for each group.
    """
    group = [disaggregation_column] if legend_column is None else [legend_column, disaggregation_column]

    subcase_duration = _get_duration_between_activities(el, 'Authorization', 'Procurement', group)

    return MultiDataSeries.from_pandas(subcase_duration, 'Authorization to procurement')


def _get_duration_between_activities(el: pd.DataFrame, start_activity: str, end_activity: str, group: list[str]) -> \
        pd.DataFrame:
    """
    Calculate the duration between two activities based on specified disaggregation attributes in the event log.

    Args:
        el (pd.DataFrame): The event log.
        start_activity (str): The start activity.
        end_activity (str): The end activity.
        group (list[str]): The columns used for grouping.

    Returns:
        pd.DataFrame: The duration between two activities based on specified disaggregation attributes in the event log.
    """
    # filter only the subcases between start_activity and end_activity
    variant = filter_between(el, start_activity, end_activity)
    # calculate the duration of each subcase
    subcase_duration = variant.groupby(group) \
        .apply(lambda x: get_all_case_durations(x)) \
        .explode() \
        .groupby(group) \
        .mean()
    return subcase_duration
