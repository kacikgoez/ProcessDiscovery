import pandas as pd

from backend.src.dataclasses.attributes import PatientAttribute
from backend.src.dataclasses.charts import Graph, MultiDataSeries, DataSeries, Variant
from backend.src.dataclasses.requests import KpiRequest, KpiType, VariantListRequest, DistributionRequest, DfgRequest
from backend.src.process_mining.event_log import load_event_log, load_patient_attributes, create_bins, filter_log, \
    load_filter_attributes
from backend.src.process_mining import kpi, dfg
from backend.src.process_mining import distribution
from backend.src.process_mining.variants import get_variants_with_frequencies
from definitions import CLEAN_EVENT_LOG_PATH


class ProcessMiningService:
    def __init__(self):
        self.event_log: pd.DataFrame = load_event_log(CLEAN_EVENT_LOG_PATH)
        self.patient_attributes: list[PatientAttribute] = load_patient_attributes(self.event_log)
        self.filter_attributes: list[PatientAttribute] = load_filter_attributes(self.event_log)

    def get_patient_attributes(self) -> list[PatientAttribute]:
        return self.patient_attributes

    def get_process_attributes(self) -> list[PatientAttribute]:
        return self.filter_attributes

    def get_variants(self, request: VariantListRequest) -> list[Variant]:
        el = filter_log(self.event_log, request.filters)
        el, dac = create_bins(el, request.disaggregation_attribute)

        return get_variants_with_frequencies(el, dac)

    def get_attribute_distribution(self, request: DistributionRequest) -> DataSeries:
        el = filter_log(self.event_log, request.filters)
        el, dac = create_bins(el, request.disaggregation_attribute)

        return distribution.attribute_distribution(el, dac)

    def get_kpi_data(self, request: KpiRequest) -> MultiDataSeries:
        el = filter_log(self.event_log, request.filters)
        el, dac = create_bins(el, request.disaggregation_attribute)
        el, lac = create_bins(el, request.legend_attribute)

        match request.kpi:
            case KpiType.HAPPY_PATH_ADHERENCE:
                return kpi.get_happy_path_adherence(el, dac, lac)
            case KpiType.DROP_OUT:
                return kpi.get_dropout(el, dac)
            case KpiType.PERMUTED_PATH_ADHERENCE:
                return kpi.get_permuted_path(el, dac, lac)
            case KpiType.BUREAUCRATIC_DURATION:
                return kpi.get_bureaucratic_duration(el, dac, lac)
            case KpiType.EVALUATION_TO_APPROACH:
                return kpi.get_evaluation_to_approach(el, dac, lac)
            case KpiType.AUTHORIZATION_TO_PROCUREMENT:
                return kpi.get_authorization_to_procurement(el, dac, lac)
            case _:
                raise ValueError('The given KPI is not supported.')

    def get_dfg(self, request: DfgRequest) -> Graph:
        el = filter_log(self.event_log, request.filters)

        return dfg.get_dfg(el)
