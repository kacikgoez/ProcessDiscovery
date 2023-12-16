from dataclasses import dataclass, field


@dataclass
class DistributionDataItem:
    """
    A data item of a distribution.

    Attributes:
        name (str): The name of the data item.
        value (float): The value of the data item.
    """
    name: str
    value: float


@dataclass
class Edge:
    """
    An edge in a graph.

    Attributes:
        source (str): The source node.
        target (str): The target node.
        label (str): The label of the edge.
        value (float): The value of the edge.
    """
    source: str
    target: str
    label: str
    value: float


@dataclass
class Node:
    """
    A node in a graph.

    Attributes:
        id (str): The id of the node.
        label (str): The label of the node.
        value (float): The value of the node.
    """
    id: str
    label: str
    value: float


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
class DataSeries:
    """
    A data series.

    Attributes:
        name (str): The name of the data series.
        data (list[dict[str, float]]): The data of the data series.
    """
    name: str
    data: list[dict[str, float]]
