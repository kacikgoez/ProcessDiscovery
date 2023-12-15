import enum
from abc import ABC
from dataclasses import dataclass

from backend.src.dataclasses.attributes import DisaggregationAttribute
from backend.src.dataclasses.filters import BaseFilter


@dataclass
class FilteredRequest(ABC):
    """
    A base request with filters.

    Attributes:
        filters (list[BaseFilter] | None): The filters of the request. Defaults to None.
    """
    filters: list[BaseFilter] | None


@dataclass
class VariantListRequest(FilteredRequest):
    """
    A request for a list of variants.

    Attributes:
        filters (list[BaseFilter] | None): The filters of the request. Defaults to None.
        disaggregation_attribute (DisaggregationAttribute): The attribute to disaggregate the variants by.
    """
    disaggregation_attribute: DisaggregationAttribute


@enum.unique
class KpiType(enum.Enum):
    """
    An enumeration of the KPI types that can be requested.
    """
    HAPPY_PATH_ADHERENCE = 'happy_path_adherence'
    """The happy path adherence KPI. The KPI measures the percentage of cases that follow the happy path."""
    DROP_OUT = 'drop_out'
    """The drop out KPI. The KPI measures the percentage of cases that drop out."""
    PERMUTED_PATH_ADHERENCE = 'permuted_path_adherence'
    """The permuted path adherence KPI. The KPI measures the percentage of cases that follow a permuted path."""
    PERMUTED_PATH_DFG = 'permuted_path_dfg'
    """The permuted path DFG KPI. This KPI measures the percentage of cases that follow a permuted path and the DFG of the permuted path."""
    BUREAUCRATIC_DURATION = 'bureaucratic_duration'
    """The bureaucratic duration KPI. This KPI measures the average bureaucratic duration."""
    EVALUATION_TO_APPROACH = 'evaluation_to_approach'
    """The evaluation to approach KPI. This KPI measures the average time from evaluation to approach."""
    AUTHORIZATION_TO_PROCUREMENT = 'authorization_to_procurement'
    """The authorization to procurement KPI. This KPI measures the average time from authorization to procurement."""


@dataclass
class KpiRequest(FilteredRequest):
    """
    A request for a KPI. The KPI will be calculated based on the given filters. The KPI will be disaggregated by the
    given disaggregation attribute. The KPI will be displayed in the legend by the given legend attribute.

    Attributes:
        filters (list[BaseFilter] | None): The filters of the request. Defaults to None.
        kpi (KpiType): The KPI to request.
        disaggregation_attribute (DisaggregationAttribute | None): The attribute to disaggregate the KPI by. Defaults to None.
        legend_attribute (DisaggregationAttribute | None): The attribute to display the KPI in the legend by. Defaults to None.
    """
    kpi: KpiType
    disaggregation_attribute: DisaggregationAttribute | None = None
    legend_attribute: DisaggregationAttribute | None = None


@dataclass
class DistributionRequest(FilteredRequest):
    """
    A request for a distribution. The distribution will be calculated based on the given filters. The distribution will
    be disaggregated by the given disaggregation attribute.

    Attributes:
        filters (list[BaseFilter] | None): The filters of the request. Defaults to None.
        disaggregation_attribute (DisaggregationAttribute): The attribute to disaggregate the distribution by.
    """
    disaggregation_attribute: DisaggregationAttribute
