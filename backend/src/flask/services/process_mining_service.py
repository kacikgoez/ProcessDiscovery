from typing import Any

import pandas as pd

from backend.src.dataclasses.attributes import CategoricalAttribute, NumericalAttribute
from backend.src.dataclasses.charts import DistributionDataItem, Graph
from backend.src.dataclasses.dataclasses import Variant
from backend.src.dataclasses.requests import KpiRequest, KpiType, VariantListRequest, DistributionRequest, DfgRequest
from backend.src.process_mining.event_log import load_event_log, load_patient_attributes, create_bins, filter_log
from backend.src.process_mining import kpi, dfg
from backend.src.process_mining import distribution
from backend.src.process_mining.variants import get_variants_with_frequencies
from definitions import CLEAN_EVENT_LOG_PATH


class ProcessMiningService:
    def __init__(self):
        self.event_log: pd.DataFrame = load_event_log(CLEAN_EVENT_LOG_PATH)
        self.patient_attributes: list[CategoricalAttribute | NumericalAttribute] = load_patient_attributes(
            self.event_log)

    def get_patient_attributes(self) -> list[CategoricalAttribute | NumericalAttribute]:
        return self.patient_attributes

    def get_variants(self, request: VariantListRequest) -> list[Variant]:
        el = filter_log(self.event_log, request.filters)

        disaggregation_attribute_column = 'disaggregation'
        el = create_bins(el, request.disaggregation_attribute, disaggregation_attribute_column)

        return get_variants_with_frequencies(el, disaggregation_attribute_column)

    def get_attribute_distribution(self, request: DistributionRequest) -> list[DistributionDataItem]:
        el = filter_log(self.event_log, request.filters)

        disaggregation_attribute_column = 'disaggregation'
        el = create_bins(el, request.disaggregation_attribute, disaggregation_attribute_column)

        return distribution.attribute_distribution(el, disaggregation_attribute_column)

    def get_kpi_data(self, request: KpiRequest) -> dict[str, list[Any]]:
        el = filter_log(self.event_log, request.filters)

        disaggregation_attribute_column = 'disaggregation'
        el = create_bins(el, request.disaggregation_attribute, disaggregation_attribute_column)

        legend_column = 'legend'
        el = create_bins(el, request.legend_attribute, legend_column)

        match request.kpi:
            case KpiType.HAPPY_PATH_ADHERENCE:
                return kpi.get_happy_path_adherence(el, disaggregation_attribute_column, legend_column)
            case KpiType.DROP_OUT:
                return kpi.get_dropout(el, disaggregation_attribute_column)
            case KpiType.PERMUTED_PATH_ADHERENCE:
                return kpi.get_permuted_path(el, disaggregation_attribute_column, legend_column)
            case KpiType.BUREAUCRATIC_DURATION:
                return kpi.get_bureaucratic_duration(el, disaggregation_attribute_column, legend_column)
            case KpiType.EVALUATION_TO_APPROACH:
                return kpi.get_evaluation_to_approach(el, disaggregation_attribute_column, legend_column)
            case KpiType.AUTHORIZATION_TO_PROCUREMENT:
                return kpi.get_authorization_to_procurement(el, disaggregation_attribute_column, legend_column)
            case _:
                raise ValueError('The given KPI is not supported.')

    def get_dfg(self, request: DfgRequest) -> Graph:
        el = filter_log(self.event_log, request.filters)

        return dfg.get_permuted_path_dfg(el)
