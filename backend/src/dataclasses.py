import enum
from dataclasses import dataclass, field
from types import UnionType


@enum.unique
class AttributeType(enum.Enum):
    """
    An enumeration of the attribute types.
    """
    CATEGORICAL = 'categorical'
    """The categorical attribute type."""
    NUMERICAL = 'numerical'
    """The numerical attribute type."""


@dataclass
class CategoricalAttribute:
    """
    A categorical attribute.

    Attributes:
        name (str): The name of the attribute.
        values (list[str]): The values of the attribute.
        type (str): The type of the attribute. Defaults to [AttributeType.CATEGORICAL][src.dataclasses.AttributeType.CATEGORICAL].
    """
    name: str
    values: list[str]
    type: str = field(init=False, default=AttributeType.CATEGORICAL.value)

    def __post_init__(self):
        self.values = sorted(self.values)


@dataclass
class NumericalAttribute:
    """
    A numerical attribute.

    Attributes:
        name (str): The name of the attribute.
        min (float): The minimum value of the attribute.
        max (float): The maximum value of the attribute.
        type (str): The type of the attribute. Defaults to [AttributeType.NUMERICAL][src.dataclasses.AttributeType.NUMERICAL].
    """
    name: str
    min: float
    max: float
    type: str = field(init=False, default=AttributeType.NUMERICAL.value)

    def __post_init__(self):
        assert self.min < self.max, 'The minimum must be smaller than the maximum.'


PatientAttribute: UnionType = CategoricalAttribute | NumericalAttribute
"""
A patient attribute. Can be either a [CategoricalAttribute][src.dataclasses.CategoricalAttribute] or a [NumericalAttribute][src.dataclasses.NumericalAttribute].
"""


@dataclass
class DisaggregationAttribute:
    """
    A disaggregation attribute.

    Attributes:
        name (str): The name of the attribute.
        type (AttributeType): The type of the attribute.
        bins (list[int], optional): The bins of the numerical attribute. Defaults to None.
    """
    name: str
    type: AttributeType
    bins: list[int] = None

    def get_bins(self, include_infinities: bool = False) -> list[float]:
        """Returns the bins of the numerical attribute.

        Example:
        ```python
        # create a numerical attribute with bins
        attribute = DisaggregationAttribute('attribute', AttributeType.NUMERICAL, bins=[0, 5, 10])

        # get the bins
        bins = attribute.get_bins(include_infinities=True)
        print(bins)
        # [-inf, 0, 5, 10, inf]
        ```

        Args:
            include_infinities (bool, optional): Whether to include the infinities in the bins. Defaults to False.

        Returns:
            list[float]: The bins.
        """
        if self.type == AttributeType.NUMERICAL:
            if include_infinities:
                return [-float('inf')] + self.bins + [float('inf')]
            else:
                return self.bins
        else:
            raise ValueError('The bins are only available for numerical attributes.')

    def get_bin_labels(self, include_infinities: bool = False) -> list[str]:
        """Returns the bin labels of the numerical attribute.

        Example:
        ```python
        # create a numerical attribute with bins
        attribute = DisaggregationAttribute('attribute', AttributeType.NUMERICAL, bins=[0, 5, 10])

        # get the bin labels
        bin_labels = attribute.get_bin_labels(include_infinities=True)
        print(bin_labels)
        # ['< 0', '0 - 5', '5 - 10', '> 10']
        ```

        Args:
            include_infinities (bool, optional): Whether to include the infinities in the bin labels. Defaults to False.

        Returns:
            list[str]: The bin labels.
        """
        if self.type == AttributeType.NUMERICAL:
            if include_infinities:
                return [f'< {self.bins[0]}'] + [f'{self.bins[i]} - {self.bins[i + 1]}' for i in
                                                range(len(self.bins) - 1)] + [f'> {self.bins[-1]}']
            else:
                return [f'{self.bins[i]} - {self.bins[i + 1]}' for i in range(len(self.bins) - 1)]
        else:
            raise ValueError('The bin labels are only available for numerical attributes.')


@dataclass
class Variant:
    """
    The data class for a variant of an event log.

    Attributes:
        activities (list[str]): The activities of the variant.
        count (int): The number of cases of the variant.
        frequency (float): The frequency of the variant.
        distribution (dict[str, int]): The distribution of the variant.
        id (int): The id of the variant.
    """
    activities: list[str]
    count: int
    frequency: float
    distribution: dict[str, int]
    id: int = field(init=False)

    def __post_init__(self):
        self.id = hash(tuple(self.activities))
