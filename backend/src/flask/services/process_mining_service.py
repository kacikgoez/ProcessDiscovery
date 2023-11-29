import pandas as pd
import pm4py

from backend.src.dataclasses import CategoricalAttribute, NumericalAttribute, DisaggregationAttribute, Variant
from backend.src.process_mining.event_log import load_event_log, load_patient_attributes
from backend.src.process_mining.variants import get_variants_with_frequencies
from typing import Any, Collection
from definitions import CLEAN_EVENT_LOG_PATH


class ProcessMiningService:
    def __init__(self):
        self.event_log: pd.DataFrame = load_event_log(CLEAN_EVENT_LOG_PATH)
        self.patient_attributes: list[CategoricalAttribute | NumericalAttribute] = load_patient_attributes(self.event_log)

    def get_variants(self, disaggregation_attribute: DisaggregationAttribute) -> list[Variant]:
        return get_variants_with_frequencies(self.event_log, disaggregation_attribute)

    def get_patient_attributes(self) -> list[CategoricalAttribute | NumericalAttribute]:
        return self.patient_attributes
