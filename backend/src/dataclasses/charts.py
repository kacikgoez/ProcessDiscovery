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

