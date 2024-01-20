import os

from backend.src.dataclasses.attributes import AttributeType

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CLEAN_EVENT_LOG_PATH = f'{ROOT_DIR}/backend/data/processed/orchid_event_log.csv'

PATIENT_ATTRIBUTES = {
    'opo_id': AttributeType.CATEGORICAL,
    'hospital_id': AttributeType.CATEGORICAL,
    'age': AttributeType.NUMERICAL,
    'gender': AttributeType.CATEGORICAL,
    'race': AttributeType.CATEGORICAL,
    'brain_death': AttributeType.CATEGORICAL,
    'referral_year': AttributeType.CATEGORICAL,
    'referral_day_of_week': AttributeType.CATEGORICAL,
    'cause_of_death': AttributeType.CATEGORICAL,
    'mechanism_of_death': AttributeType.CATEGORICAL,
    'circumstances_of_death': AttributeType.CATEGORICAL,
    # outcomes for each organ
    'outcome_heart': AttributeType.CATEGORICAL,
    'outcome_liver': AttributeType.CATEGORICAL,
    'outcome_kidney_left': AttributeType.CATEGORICAL,
    'outcome_kidney_right': AttributeType.CATEGORICAL,
    'outcome_lung_left': AttributeType.CATEGORICAL,
    'outcome_lung_right': AttributeType.CATEGORICAL,
    'outcome_pancreas': AttributeType.CATEGORICAL,
}

FILTER_ATTRIBUTES = {
    'variant': AttributeType.CATEGORICAL,
    'start_activity': AttributeType.CATEGORICAL,
    'end_activity': AttributeType.CATEGORICAL,
    'case_size': AttributeType.NUMERICAL,
    'case_duration': AttributeType.NUMERICAL,
}

SORT_ORDERS = {
    'referral_day_of_week': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
}