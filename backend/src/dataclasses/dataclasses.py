from dataclasses import dataclass, field


@dataclass
class Variant:
    """
    A variant of the process.

    Attributes:
        activities (list[str]): The activities of the variant.
        count (int): The number of occurrences of the variant.
        frequency (float): The frequency of the variant.
        distribution (dict[str, int]): The distribution of the variant based on another attribute.
        id (int): The hash of the variant.
    """
    activities: list[str]
    count: int
    frequency: float
    distribution: dict[str, int]
    id: int = field(init=False)

    def __post_init__(self):
        self.id = hash(tuple(self.activities))
