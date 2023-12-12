import os

import pandas as pd
import pm4py

from backend.src.dataclasses import CategoricalAttribute, NumericalAttribute
from backend.src.process_mining.event_log import (load_event_log,
                                                  load_patient_attributes)
from definitions import CLEAN_EVENT_LOG_PATH


class ProcessMiningService:
    def __init__(self):
        if os.path.exists(CLEAN_EVENT_LOG_PATH):
            self.event_log: pd.DataFrame = load_event_log(CLEAN_EVENT_LOG_PATH)
            self.patient_attributes: list[CategoricalAttribute |
                                          NumericalAttribute] = load_patient_attributes(self.event_log)

    def get_variants(self) -> list[tuple[str]]:
        variants = pm4py.get_variants(self.event_log)
        return variants

    def get_patient_attributes(self) -> list[CategoricalAttribute | NumericalAttribute]:
        return self.patient_attributes
