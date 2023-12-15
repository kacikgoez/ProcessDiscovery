import enum
from abc import ABC
from dataclasses import dataclass

from backend.src.dataclasses.attributes import DisaggregationAttribute
from backend.src.dataclasses.filters import BaseFilter


@dataclass
class FilteredRequest(ABC):
    filters: list[BaseFilter] | None


@dataclass
class VariantListRequest(FilteredRequest):
    disaggregation_attribute: DisaggregationAttribute


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
class KpiRequest(FilteredRequest):
    kpi: KpiType
    disaggregation_attribute: DisaggregationAttribute | None = None
    legend_attribute: DisaggregationAttribute | None = None


@dataclass
class DistributionRequest(FilteredRequest):
    disaggregation_attribute: DisaggregationAttribute
