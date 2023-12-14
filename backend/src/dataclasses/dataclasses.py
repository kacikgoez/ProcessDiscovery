from dataclasses import dataclass, field


@dataclass
class Variant:
    activities: list[str]
    count: int
    frequency: float
    distribution: dict[str, int]
    id: int = field(init=False)

    def __post_init__(self):
        self.id = hash(tuple(self.activities))
