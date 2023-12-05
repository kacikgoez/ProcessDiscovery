import enum
from dataclasses import dataclass, field


@enum.unique
class AttributeType(enum.Enum):
    CATEGORICAL = 'categorical'
    NUMERICAL = 'numerical'


@dataclass
class CategoricalAttribute:
    name: str
    values: list[str]
    type: str = field(init=False, default=AttributeType.CATEGORICAL.value)

    def __post_init__(self):
        self.values = sorted(self.values)


@dataclass
class NumericalAttribute:
    name: str
    min: float
    max: float
    type: str = field(init=False, default=AttributeType.NUMERICAL.value)

    def __post_init__(self):
        {}  #assert self.min < self.max, 'The minimum must be smaller than the maximum.'


@dataclass
class DisaggregationAttribute:
    name: str
    type: AttributeType
    bins: list[int] = None

    def get_bins(self, include_infinities: bool = False) -> list[float]:
        """Returns the bins of the numerical attribute.

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
    activities: list[str]
    count: int
    frequency: float
    distribution: dict[str, int]
    id: int = field(init=False)

    def __post_init__(self):
        self.id = hash(tuple(self.activities))


@enum.unique
class KpiType(enum.Enum):
    HAPPY_PATH_ADHERENCE = 'happy_path_adherence'
    DROP_OUT = 'drop_out'
    PERMUTED_PATH_ADHERENCE = 'permuted_path_adherence'
    PERMUTED_PATH_DFG = 'permuted_path_dfg'
    BUREAUCRATIC_DURATION = 'bureaucratic_duration'
    EVALUATION_TO_APPROACH = 'evaluation_to_approach'
    AUTHORIZATION_TO_PROCUREMENT = 'authorization_to_procurement'


@dataclass
class KpiRequest:
    kpi: KpiType
    disaggregation_attribute: DisaggregationAttribute | None = None
    legend_attribute: DisaggregationAttribute | None = None
