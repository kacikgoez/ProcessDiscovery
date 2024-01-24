import pandas as pd
from pm4py.filtering import filter_variants
from pm4py.discovery import discover_dfg, discover_performance_dfg
from backend.src.dataclasses.charts import Graph, Edge, Node


DE_JURE_VARIANT = ('Referral', 'Evaluation', 'Approach', 'Authorization', 'Procurement', 'Transplant')


def get_dejure_variant(el: pd.DataFrame) -> pd.DataFrame:
    """
     Extracts the dejure variants from the input DataFrame.

     Args:
         el (pd.DataFrame): The event log.

     Returns:
         pd.DataFrame: A DataFrame representing all cease of the dejure variants.
     """
    # compute the variants to filter
    dejure_list = [DE_JURE_VARIANT[:i + 1] for i in range(len(DE_JURE_VARIANT))]

    # filter only dejure variant
    variant = filter_variants(el, dejure_list, retain=True)

    return variant


def get_dejure_remain_graph(el: pd.DataFrame, disaggregation_column: str) -> Graph:
    """
        Generates a graph representing the dejure DFG with activity frequencies
        and the percentage of each activity that goes to the next activity
        considering a specified disaggregation column.

        Args:
            el (pd.DataFrame): The event log.
            disaggregation_column (str): Disaggregation attribute column

        Returns:
            Graph: A Graph object representing the dejure DFG
            with activity frequencies and percentage.
        """

    # Drop the disaggregation_column of nan and calculate the frequency of each activity
    act_freq = el.dropna(subset=[disaggregation_column])['concept:name'].value_counts()
    nodes = [Node(id=value, label=value, value=count) for value, count in act_freq.items()]

    variant = get_dejure_variant(el)

    # Group the dejure cases by disaggregation_column, disregarding the disaggregation_column of nan
    grouped_dfg = variant.groupby(disaggregation_column, observed=False).apply(lambda x: discover_dfg(x)[0])

    all_edges = []

    # Calculate the percentage of one activity that goes to the next activity
    for index, relation in grouped_dfg.items():
        edges = [Edge(source=source, target=target, label=index, value=freq / act_freq[source])
                 for (source, target), freq in relation.items()]
        all_edges.extend(edges)

    return Graph(
        name='Dejure-DFG',
        edges=all_edges,
        nodes=nodes,
    )


def get_dejure_drop_graph(el: pd.DataFrame, disaggregation_column: str) -> Graph:
    """ Generates a graph representing the dejure DFG with counts of end activities
        and the dropout rate of each activity considering a specified disaggregation
        column.

        Args:
            el (pd.DataFrame): The event log.
            disaggregation_column (str): Disaggregation attribute column

       Returns:
           Graph: A Graph object representing the dejure DFG
            with drop out information.
       """

    # Calculate the end activity counts considering disaggregation column
    disaggregation_last_act = el.groupby(by=['case:concept:name']).last()[[disaggregation_column,
                                                                           'concept:name']].value_counts()
    # Calculate the end activity counts
    last_act_freq = disaggregation_last_act.groupby('concept:name').sum()
    nodes = [Node(id=value, label=value, value=count) for value, count in last_act_freq.items()]
    nodes.append(Node(id='Referral', label='Referral', value=0))

    variant = get_dejure_variant(el)

    # Group the dejure cases by disaggregation_column, disregarding the disaggregation_column of nan
    grouped_dfg = variant.groupby(disaggregation_column, observed=False).apply(lambda x: discover_dfg(x)[0])

    all_edges = []

    # Calculate the percentage of one activity that goes to the next activity
    for index, relation in grouped_dfg.items():
        edges = [
            Edge(source=source, target=target, label=index,
                value=(disaggregation_last_act.loc[index, source] / last_act_freq[source]) if last_act_freq.get(
                    source, 0) != 0 else 0
            )
            for (source, target), freq in relation.items()
        ]
        all_edges.extend(edges)

    return Graph(
        name='Dejure-DFG',
        edges=all_edges,
        nodes=nodes,
    )


def get_dejure_time_graph(el: pd.DataFrame, disaggregation_column: str, statistic: str) -> Graph:
    """
        Generates a graph representing the dejure DFG with performance
        statistics considering a specified disaggregation attribute.

        Args:
            el (pd.DataFrame): The event log.
            disaggregation_column (str): Disaggregation attribute column.
            statistic (str): The performance statistic to be considered.

        Returns:
            Graph: A Graph object representing the dejure DFG
            with performance statistics.
        """

    # Drop the disaggregation_column of nan and calculate the frequency of each activity
    act_freq = el.dropna(subset=[disaggregation_column])['concept:name'].value_counts()
    nodes = [Node(id=value, label=value, value=count) for value, count in act_freq.items()]

    variant = get_dejure_variant(el)

    # Group the dejure cases by disaggregation_column, disregarding the disaggregation_column of nan
    grouped_dfg = variant.groupby(disaggregation_column, observed=False).apply(lambda x: discover_performance_dfg(x)[0])

    all_edges = []
    for index, relation in grouped_dfg.items():
        edges = [Edge(source=source, target=target, label=index, value=performance[statistic] / 60)
                 for (source, target), performance in relation.items()]
        all_edges.extend(edges)

    return Graph(
        name='Dejure-DFG',
        edges=all_edges,
        nodes=nodes,
    )
