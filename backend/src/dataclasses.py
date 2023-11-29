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
class Interval:
    lower: float
    upper: float

    def __post_init__(self):
        assert self.lower < self.upper, 'The lower bound must be smaller than the upper bound.'


@dataclass
class NumericalAttribute:
    name: str
    min: float
    max: float
    groups: list[Interval] = None
    type: str = field(init=False, default=AttributeType.NUMERICAL.value)

    def __post_init__(self):
        assert self.min < self.max, 'The minimum must be smaller than the maximum.'

    def create_groups(self, n: int) -> 'NumericalAttribute':
        """Create n equally sized groups for the numerical attribute.

        Args:
            n (int): The number of groups.
        """
        self.groups = []
        step = (self.max - self.min) / n
        for i in range(n):
            lower = self.min + i * step
            upper = lower + step
            self.groups.append(Interval(lower, upper))
        return self
