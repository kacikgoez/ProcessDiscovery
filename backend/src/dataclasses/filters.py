import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass


@enum.unique
class FilterOperator(enum.Enum):
    """
    An enumeration of the supported filter operators.
    """
    IS_EMPTY = 'is_empty'
    """The is empty operator."""
    IS_NOT_EMPTY = 'is_not_empty'
    """The is not empty operator."""
    EQUALS = 'equals'
    """The equals operator."""
    NOT_EQUALS = 'not_equals'
    """The not equals operator."""
    CONTAINS = 'contains'
    """The contains operator."""
    NOT_CONTAINS = 'not_contains'
    """The not contains operator."""
    LESS_THAN = 'less_than'
    """The less than operator."""
    LESS_THAN_OR_EQUALS = 'less_than_or_equals'
    """The less than or equals operator."""
    GREATER_THAN = 'greater_than'
    """The greater than operator."""
    GREATER_THAN_OR_EQUALS = 'greater_than_or_equals'
    """The greater than or equals operator."""

    @property
    def accepts_no_value(self) -> bool:
        """
        Returns whether the operator accepts no value.

        Returns:
            (bool): Whether the operator accepts no value.
        """
        return self in [
            FilterOperator.IS_EMPTY,
            FilterOperator.IS_NOT_EMPTY]

    @property
    def accepts_single_value(self):
        """
        Returns whether the operator accepts a single value.

        Returns:
            (bool): Whether the operator accepts a single value.
        """
        return self in [
            FilterOperator.EQUALS,
            FilterOperator.NOT_EQUALS,
            FilterOperator.LESS_THAN,
            FilterOperator.LESS_THAN_OR_EQUALS,
            FilterOperator.GREATER_THAN,
            FilterOperator.GREATER_THAN_OR_EQUALS]

    @property
    def accepts_multiple_values(self) -> bool:
        """
        Returns whether the operator accepts multiple values.

        Returns:
            (bool): Whether the operator accepts multiple values.
        """
        return self in [
            FilterOperator.CONTAINS,
            FilterOperator.NOT_CONTAINS]


@dataclass
class BaseFilter(ABC):
    """
    A base filter.

    Attributes:
        attribute_name (str): The name of the attribute.
        operator (FilterOperator): The operator of the filter.
    """
    attribute_name: str
    operator: FilterOperator

    def __post_init__(self):
        assert self.operator in self.supported_operators(), 'The operator is not supported for this type of attribute.'

    @property
    @abstractmethod
    def filter_value(self) -> list[str] | str | float | None:
        """
        Returns the value to filter for.

        Returns:
            (list[str] | str | float | None): The value to filter for.
        """
        pass

    @classmethod
    @abstractmethod
    def supported_operators(cls) -> tuple[FilterOperator, ...]:
        """
        Returns the supported operators for the filter.

        Returns:
            (tuple[FilterOperator, ...]): The supported operators for the filter.
        """
        pass


@dataclass
class CategoricalFilter(BaseFilter):
    """
    A categorical filter. The filter can be used to filter for categorical attributes.
    Currently, the filter supports the following operators:

    - [IS_EMPTY][backend.src.dataclasses.filters.FilterOperator.IS_EMPTY]
    - [NOT_EMPTY][backend.src.dataclasses.filters.FilterOperator.IS_NOT_EMPTY]
    - [EQUALS][backend.src.dataclasses.filters.FilterOperator.EQUALS]
    - [NOT_EQUALS][backend.src.dataclasses.filters.FilterOperator.NOT_EQUALS]
    - [CONTAINS][backend.src.dataclasses.filters.FilterOperator.CONTAINS]
    - [NOT_CONTAINS][backend.src.dataclasses.filters.FilterOperator.NOT_CONTAINS]

    Attributes:
        values (list[str] | None): The values to filter for.
    """
    values: list[str] | None

    @classmethod
    def supported_operators(cls) -> tuple[FilterOperator, ...]:
        """
        Returns the supported operators for the filter.

        Returns:
            (tuple[FilterOperator, ...]): The supported operators for the filter.
        """
        return (
            FilterOperator.IS_EMPTY,
            FilterOperator.IS_NOT_EMPTY,
            FilterOperator.EQUALS,
            FilterOperator.NOT_EQUALS,
            FilterOperator.CONTAINS,
            FilterOperator.NOT_CONTAINS)

    @property
    def filter_value(self) -> list[str] | str | None:
        """
        Returns the value to filter for. If the operator does not accept a value, None is returned.
        If the operator accepts multiple values, the values are returned as a list,
        otherwise the first value is returned.

        Returns:
            (list[str] | str | None): The value to filter for.
        """
        if self.operator.accepts_no_value:
            return None
        if self.operator.accepts_single_value:
            return self.values[0]
        else:
            return self.values

    def __repr__(self):
        return f'{self.attribute_name} {self.operator.value} {self.filter_value}'


@dataclass
class NumericalFilter(BaseFilter):
    """
    A numerical filter. The filter can be used to filter for numerical attributes.
    Currently, the filter supports the following operators:

    - [IS_EMPTY][backend.src.dataclasses.filters.FilterOperator.IS_EMPTY]
    - [NOT_EMPTY][backend.src.dataclasses.filters.FilterOperator.IS_NOT_EMPTY]
    - [EQUALS][backend.src.dataclasses.filters.FilterOperator.EQUALS]
    - [NOT_EQUALS][backend.src.dataclasses.filters.FilterOperator.NOT_EQUALS]
    - [LESS_THAN][backend.src.dataclasses.filters.FilterOperator.LESS_THAN]
    - [LESS_THAN_OR_EQUALS][backend.src.dataclasses.filters.FilterOperator.LESS_THAN_OR_EQUALS]
    - [GREATER_THAN][backend.src.dataclasses.filters.FilterOperator.GREATER_THAN]
    - [GREATER_THAN_OR_EQUALS][backend.src.dataclasses.filters.FilterOperator.GREATER_THAN_OR_EQUALS]

    Attributes:
        value (float | None): The value to filter for.
    """
    value: float | None

    @classmethod
    def supported_operators(cls) -> tuple[FilterOperator, ...]:
        """
        Returns the supported operators for the filter.

        Returns:
            (tuple[FilterOperator, ...]): The supported operators for the filter.
        """
        return (
            FilterOperator.IS_EMPTY,
            FilterOperator.IS_NOT_EMPTY,
            FilterOperator.EQUALS,
            FilterOperator.NOT_EQUALS,
            FilterOperator.LESS_THAN,
            FilterOperator.LESS_THAN_OR_EQUALS,
            FilterOperator.GREATER_THAN,
            FilterOperator.GREATER_THAN_OR_EQUALS)

    @property
    def filter_value(self) -> float | None:
        """
        Returns the value to filter for.

        Returns:
            (float | None): The value to filter for.
        """
        return self.value

    def __repr__(self):
        return f'{self.attribute_name} {self.operator.value} {self.filter_value}'
