import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass


@enum.unique
class FilterOperator(enum.Enum):
    EQUALS = 'equals'
    NOT_EQUALS = 'not_equals'
    CONTAINS = 'contains'
    NOT_CONTAINS = 'not_contains'
    LESS_THAN = 'less_than'
    LESS_THAN_OR_EQUALS = 'less_than_or_equals'
    GREATER_THAN = 'greater_than'
    GREATER_THAN_OR_EQUALS = 'greater_than_or_equals'

    @property
    def accepts_multiple_values(self):
        return self in [
            FilterOperator.CONTAINS,
            FilterOperator.NOT_CONTAINS]

    @property
    def accepts_single_value(self):
        return self in [
            FilterOperator.EQUALS,
            FilterOperator.NOT_EQUALS,
            FilterOperator.LESS_THAN,
            FilterOperator.LESS_THAN_OR_EQUALS,
            FilterOperator.GREATER_THAN,
            FilterOperator.GREATER_THAN_OR_EQUALS]


@dataclass
class BaseFilter(ABC):
    attribute_name: str
    operator: FilterOperator

    @property
    @abstractmethod
    def filter_value(self) -> list[str] | str | float:
        pass

    @classmethod
    @abstractmethod
    def supported_operators(cls) -> list[FilterOperator]:
        pass


@dataclass
class CategoricalFilter(BaseFilter):
    values: list[str]

    def __post_init__(self):
        assert self.operator in self.supported_operators(), 'The operator is not supported for categorical attributes.'

    @classmethod
    def supported_operators(cls) -> list[FilterOperator]:
        return [
            FilterOperator.EQUALS,
            FilterOperator.NOT_EQUALS,
            FilterOperator.CONTAINS,
            FilterOperator.NOT_CONTAINS]

    @property
    def filter_value(self) -> list[str] | str:
        if self.operator.accepts_single_value:
            return self.values[0]
        else:
            return self.values

    def __repr__(self):
        return f'{self.attribute_name} {self.operator.value} {self.filter_value}'


@dataclass
class NumericalFilter(BaseFilter):
    value: float

    def __post_init__(self):
        assert self.operator in self.supported_operators(), 'The operator is not supported for numerical attributes.'

    @classmethod
    def supported_operators(cls) -> list[FilterOperator]:
        return [
            FilterOperator.EQUALS,
            FilterOperator.NOT_EQUALS,
            FilterOperator.LESS_THAN,
            FilterOperator.LESS_THAN_OR_EQUALS,
            FilterOperator.GREATER_THAN,
            FilterOperator.GREATER_THAN_OR_EQUALS]

    @property
    def filter_value(self) -> float:
        return self.value

    def __repr__(self):
        return f'{self.attribute_name} {self.operator.value} {self.filter_value}'
