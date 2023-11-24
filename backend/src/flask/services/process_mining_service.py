from typing import Any, Collection

import pandas as pd

from backend.src.process_mining.variants import get_variants_with_frequencies
from definitions import CLEAN_EVENT_LOG_PATH


class ProcessMiningService:
    def __init__(self):
        print("ProcessMiningService created")
        # Load the event log
        df = pd.read_csv(CLEAN_EVENT_LOG_PATH, sep=',')
        # Convert the time columns to datetime
        df['time:timestamp'] = pd.to_datetime(df['time:timestamp'], format='ISO8601')
        # Get the columns currently stored as objects
        object_columns = df.select_dtypes(include=['object']).columns
        # Remove the columns that are not categorical
        object_columns = object_columns.drop(['concept:name', 'case:concept:name'])
        # Convert the object columns to categorical columns
        df[object_columns] = df[object_columns].astype('category')
        # Store the event log
        self.event_log = df

    def get_variants(self) -> list[dict[str, Collection[str] | int | Any]]:
        return get_variants_with_frequencies(self.event_log, 'gender')
