import pandas as pd
import pm4py

from backend.src.process_mining.event_log import load_event_log
from definitions import CLEAN_EVENT_LOG_PATH


class ProcessMiningService:
    def __init__(self):
        self.event_log = load_event_log(CLEAN_EVENT_LOG_PATH)
        self.patient_attributes

    def get_variants(self) -> list[tuple[str]]:
        variants = pm4py.get_variants(self.event_log)
        return variants
