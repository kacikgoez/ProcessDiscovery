import pandas as pd
import pytest

from app import CLEAN_EVENT_LOG_PATH
from backend.src.data.extract import PATIENT_DATA_MAPPING


class TestEventLogExtraction:
    @pytest.fixture
    def event_log(self):
        return pd.read_csv(CLEAN_EVENT_LOG_PATH)

    def test_event_log_exists(self, event_log):
        assert not event_log.empty

    def test_all_columns_exist(self, event_log):
        expected_columns = [
            'case:concept:name',    # The case id
            'concept:name',         # The activity name
            'time:timestamp',       # The timestamp of the activity
        ] + list(PATIENT_DATA_MAPPING.values())  # The patient data

        for col in expected_columns:
            assert col in event_log.columns

    def test_no_missing_case_ids(self, event_log):
        assert not event_log['case:concept:name'].isna().any()

    def test_no_missing_activity_names(self, event_log):
        assert not event_log['concept:name'].isna().any()

    def test_no_missing_timestamps(self, event_log):
        assert not event_log['time:timestamp'].isna().any()

    def test_only_valid_activities(self, event_log):
        allowed_activities = ['Referral', 'Evaluation', 'Approach', 'Authorization', 'Procurement', 'Transplant']
        assert event_log['concept:name'].isin(allowed_activities).all()

    def test_only_valid_outcomes(self, event_log):
        allowed_outcomes = ['Transplanted', 'Recovered for Research', 'Recovered for Transplant but not Transplanted']
        outcome_columns = [c for c in PATIENT_DATA_MAPPING.keys() if c.startswith('outcome_')]

        for col in outcome_columns:
            assert event_log[col].dropna().isin(allowed_outcomes).all()
