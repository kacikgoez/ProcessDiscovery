import pandas as pd

from backend.src.dataclasses.attributes import (AttributeType,
                                                CategoricalAttribute,
                                                DisaggregationAttribute,
                                                NumericalAttribute,
                                                PatientAttribute)
from backend.src.dataclasses.charts import (DataSeries, DistributionDataItem,
                                            Graph, MultiDataSeries, Variant)
from backend.src.dataclasses.requests import (DejureGraphRequest,
                                              DejureStatisticType, DfgRequest,
                                              DistributionRequest, KpiRequest,
                                              KpiType, VariantListRequest)
from backend.src.process_mining import dejure, dfg, distribution, kpi
from backend.src.process_mining.event_log import (create_bins, filter_log,
                                                  load_event_log,
                                                  load_filter_attributes,
                                                  load_patient_attributes)
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

    def get_dejure_graph(self, request: DejureGraphRequest) -> Graph:
        el = filter_log(self.event_log, request.filters)

        disaggregation_attribute_column = 'disaggregation'
        el = create_bins(el, request.disaggregation_attribute)

        match request.statistic:
            case DejureStatisticType.MIN:
                return dejure.get_dejure_time_graph(el, disaggregation_attribute_column, 'min')
            case DejureStatisticType.MAX:
                return dejure.get_dejure_time_graph(el, disaggregation_attribute_column, 'max')
            case DejureStatisticType.MEAN:
                return dejure.get_dejure_time_graph(el, disaggregation_attribute_column, 'mean')
            case DejureStatisticType.MEDIAN:
                return dejure.get_dejure_time_graph(el, disaggregation_attribute_column, 'median')
            case DejureStatisticType.REMAIN:
                return dejure.get_dejure_remain_graph(el, disaggregation_attribute_column)
            case DejureStatisticType.DROP:
                return  dejure.get_dejure_drop_graph(el, disaggregation_attribute_column)
            case _:
                raise ValueError('The given statistic is not supported.')

