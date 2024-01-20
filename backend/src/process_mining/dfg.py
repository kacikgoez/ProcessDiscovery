import pandas as pd
from pm4py import discover_dfg

from backend.src.dataclasses.charts import Graph, Edge, Node


def get_dfg(el: pd.DataFrame) -> Graph:
    """
    Generate a Process Mining DFG based on the given event log.

    Args:
        el (pd.DataFrame): The event log.

    Returns:
        (Graph): The DFG of the event log with absolute frequencies as edge values.
    """

    # find the directly-following graph
    dfg, start_activities, end_activities = discover_dfg(el)

    # transform into graph data structure
    edges = [Edge(source=source, target=target, label=None, value=freq) for (source, target), freq in dfg.items()]
    node_ids = set([edge.source for edge in edges] + [edge.target for edge in edges])
    nodes = [Node(id=activity, label=activity, value=None) for activity in node_ids]

    return Graph(
        name='DFG',
        edges=edges,
        nodes=nodes,
    )
