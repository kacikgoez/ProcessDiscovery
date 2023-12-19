from typing import Dict, List
import pandas as pd
from pm4py import discover_dfg

DE_JURE_VARIANT = ('Referral', 'Evaluation', 'Approach', 'Authorization', 'Procurement', 'Transplant')


def get_permuted_path_dfg(el: pd.DataFrame, disaggregation_column: str) -> Dict[str, List[Dict[str, str | int]]]:
    """
    Generate a Process Mining Directly-Follows Graph (DFG) based on the given event log.

    Args:
        el (pd.DataFrame): The event log DataFrame containing process data.
        disaggregation_column (str): The column name based on which the event log is disaggregated.
            This column represents the distinct groups for DFG analysis.

    Returns:
        Dict[str, List[Dict[str, Union[str, int]]]]: A dictionary containing:
            - 'nodes': A list of dictionaries representing nodes with activities and coordinates.
            - 'links': A list of dictionaries representing directly-following relationships.
    """

    # find the directly-following graph
    dfg = el.groupby(disaggregation_column).apply(lambda x: discover_dfg(x, case_id_key='case:concept:name',
                                                        activity_key='concept:name', timestamp_key='time:timestamp')[0])

    nodes = []
    links = []
    coordinates = {}
    rank = 0
    for index, row in dfg.items():
        rank = rank + 1
        for pair, freq in row.items():
            # find directly-following relations
            links.append(
                {
                    'source': pair[0] + "_" + str(index),
                    'target': pair[1] + "_" + str(index),
                    'value': freq
                }
            )

        # Assign coordinates based on activity values
        for key, value in enumerate(DE_JURE_VARIANT):
            coordinates[value + "_" + str(index)] = {'x': rank * 5, 'y': key + 20}

            nodes.append(
                {
                    'name': value + "_" + str(index),
                    'x': coordinates[value+ "_" + str(index)]['x'],
                    'y': coordinates[value+ "_" + str(index)]['y']
                }
            )

    return {"nodes": nodes, "links": links}


