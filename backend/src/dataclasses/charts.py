from dataclasses import dataclass

import pandas as pd

from definitions import SORT_ORDERS


@dataclass
class Edge:
    """
    An edge in a graph.

    Attributes:
        source (str): The source node.
        target (str): The target node.
        label (str | None): The label of the edge.
        value (float | None): The value of the edge.
    """
    source: str
    target: str
    label: str | None
    value: float | None


@dataclass
class Node:
    """
    A node in a graph.

    Attributes:
        id (str): The id of the node.
        label (str): The label of the node.
        value (float | None): The value of the node.
    """
    id: str
    label: str
    value: float | None


@dataclass
class Graph:
    """
    A graph.

    Attributes:
        name (str): The name of the graph.
        nodes (list[Node]): The nodes of the graph.
        edges (list[Edge]): The edges of the graph.
    """
    name: str
    nodes: list[Node]
    edges: list[Edge]

    def __post_init__(self):
        """
        Check that the nodes have unique ids and that the edges are valid.

        Raises:
            ValueError: If the node ids are not unique or if an edge is invalid.
        """
        if len([node.id for node in self.nodes]) != len(set([node.id for node in self.nodes])):
            raise ValueError('The node ids are not unique.')
        node_ids = [node.id for node in self.nodes]
        for edge in self.edges:
            if edge.source not in node_ids or edge.target not in node_ids:
                raise ValueError('The edge is invalid.')


@dataclass
class DataItem:
    """
    A data item.

    Attributes:
        x (str | int | float): The x value of the data item.
        y (float): The y value of the data item.
    """
    x: str | int | float
    y: float


@dataclass
class DataSeries:
    """
    A data series.

    Attributes:
        name (str): The name of the data series.
        data (list[DataItem]): The data of the data series.
    """
    name: str
    data: list[DataItem]

    @classmethod
    def from_dict(cls, name: str, data: dict[str | int | float, float], sort_by: str | None = None) -> "DataSeries":
        """
        Create a data series from a dictionary. The keys of the dictionary will be used as x values and the values of
        the dictionary will be used as y values. The data will be sorted by the x values. If the sort_by parameter is
        given and a sort order is defined for the given key, the data will be sorted by the sort order.

        Args:
            name (str): The name of the data series.
            data (dict[str | int | float, float]): The data of the data series.
            sort_by (str | None): The key to sort the data by.

        Returns:
            DataSeries: The data series.
        """

        # sort the data by the x values
        if sort_by in SORT_ORDERS:
            data = dict(sorted(data.items(), key=lambda item: SORT_ORDERS[sort_by].index(item[0])))
        else:
            data = dict(sorted(data.items(), key=lambda item: item[0]))

        return DataSeries(name=name, data=[DataItem(x=x, y=y) for x, y in data.items()])


@dataclass
class MultiDataSeries:
    """
    A data series.

    Attributes:
        name (str): The name of the data series.
        series (list[DataItem]): The series of the data series.
    """
    name: str
    series: list[DataSeries]

    @classmethod
    def from_pandas(cls, df: pd.DataFrame | pd.Series, name: str) -> "MultiDataSeries":
        """
        Create a data series from a pandas series. The index of the pandas series must have one or two levels. If the
        index has one level, the data series will contain one series. If the index has two levels, the data series will
        contain multiple series (one for each value of the first level).

        Args:
            df (pd.Series): The data of the data series.
            name (str): The name of the data series.

        Returns:
            MultiDataSeries: The data series.
        """
        series = []
        if df.index.nlevels == 1:
            series.append(DataSeries.from_dict(
                name=name,
                data=df.to_dict(),
                sort_by=df.index.name
            ))
        elif df.index.nlevels == 2:
            for index, row in df.unstack().iterrows():
                series.append(DataSeries.from_dict(
                    name=str(index),
                    data=row.to_dict(),
                    sort_by=df.index.names[1]
                ))
        else:
            raise ValueError('The index has more than two levels.')

        return MultiDataSeries(
            name=name,
            series=series,
        )
