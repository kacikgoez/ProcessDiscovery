import pandas as pd
from pandas import Timedelta

from definitions import ROOT_DIR, CLEAN_EVENT_LOG_PATH, PATIENT_ATTRIBUTES

"""
This script is used to extract an event log from the original data.
We use the Organ Retrieval and Collection of Health Information for Donation (ORCHID) dataset https://doi.org/10.13026/eytj-4f29.
As the dataset is not publicly available, we cannot provide the data here.
You can request access to the data and place the `opd.csv` file in the `data/raw` folder.
"""

RAW_DATASET = 'opd.csv'

# The mapping from the original column names to the new column names
PATIENT_DATA_MAPPING = {
    'PatientID': 'case:concept:name',  # The case id
    'OPO': 'opo_id',
    'HospitalID': 'hospital_id',
    'Age': 'age',
    'Gender': 'gender',
    'Race': 'race',
    'brain_death': 'brain_death',
    'Referral_Year': 'referral_year',  # interesting as the time attributes are randomly shifted
    'Referral_DayofWeek': 'referral_day_of_week',  # interesting as the time attributes are randomly shifted
    'Cause_of_Death_UNOS': 'cause_of_death',
    'Mechanism_of_Death': 'mechanism_of_death',
    'Circumstances_of_Death': 'circumstances_of_death',
    # outcomes for each organ
    'outcome_heart': 'outcome_heart',
    'outcome_liver': 'outcome_liver',
    'outcome_kidney_left': 'outcome_kidney_left',
    'outcome_kidney_right': 'outcome_kidney_right',
    'outcome_lung_left': 'outcome_lung_left',
    'outcome_lung_right': 'outcome_lung_right',
    'outcome_pancreas': 'outcome_pancreas',
}


def extract(raw: pd.DataFrame) -> pd.DataFrame:
    """
    This function extracts an event log from the raw data.

    Steps:
        1. Convert all time columns to datetime
        2. Only keep allowed categories for the outcome columns
        3. Iterate over all rows that correspond to a patient and add all events that happened to the patient to the event list
        4. Transform the event list to a dataframe
        5. Remove cases with missing timestamps
        6. Sort the event log by patient id and time


    Args:
        raw (pd.DataFrame): The raw data

    Returns:
        (pd.DataFrame): The extracted event log
    """
    # Convert all time columns to datetime
    time_columns = ['time_referred', 'time_approached', 'time_authorized', 'time_procured']
    for col in time_columns:
        raw[col] = pd.to_datetime(raw[col], format='ISO8601')

    # Only keep allowed outcomes
    allowed_outcomes = ['Transplanted', 'Recovered for Research', 'Recovered for Transplant but not Transplanted']
    include_outcomes = [c for c in PATIENT_DATA_MAPPING.keys() if c.startswith('outcome_')]
    for col in include_outcomes:
        raw[col] = raw[col].astype('category').cat.set_categories(allowed_outcomes)

    events_list = []
    # Iterate over all rows that correspond to a patient and add all events that happened to the patient to the event list
    for i, row in raw.iterrows():
        # Collect patient data by mapping the original column names to the new column names
        patient_data = {v: row[k] for k, v in PATIENT_DATA_MAPPING.items()}

        # Add the referral and evaluation events for each patient as all patients were referred and evaluated
        events_list.append({'concept:name': 'Referral', 'time:timestamp': row['time_referred']} | patient_data)

        # Unfortunately, the evaluation time is not available in the dataset
        # We assume that the evaluation happens one minute after the referral
        events_list.append(
            {'concept:name': 'Evaluation',
             'time:timestamp': row['time_referred'] + Timedelta(minutes=1)} | patient_data)

        # Add each activity only if its corresponding entry is not False
        if row['approached']:
            events_list.append({'concept:name': 'Approach', 'time:timestamp': row['time_approached']} | patient_data)

        if row['authorized']:
            events_list.append(
                {'concept:name': 'Authorization', 'time:timestamp': row['time_authorized']} | patient_data)

        if row['procured']:
            events_list.append({'concept:name': 'Procurement', 'time:timestamp': row['time_procured']} | patient_data)

        # Unfortunately, the transplant time is not available in the dataset
        # We assume that the transplant happens one minute after the procurement
        if row['transplanted']:
            events_list.append({'concept:name': 'Transplant',
                                'time:timestamp': row['time_procured'] + Timedelta(minutes=1)} | patient_data)

    # Transform the event list to a dataframe
    columns = ['case:concept:name', 'concept:name', 'time:timestamp'] + list(PATIENT_ATTRIBUTES.keys())
    event_log = pd.DataFrame(events_list, columns=columns)

    # Get cases where a timestamp is missing
    cases_with_missing_timestamps = event_log[event_log['time:timestamp'].isna()]['case:concept:name'].unique()
    print(f'Found {len(cases_with_missing_timestamps)} cases with missing timestamps. Removing them ...')

    # Remove cases with missing timestamps
    event_log = event_log[~event_log['case:concept:name'].isin(cases_with_missing_timestamps)]

    # Sort the event log by patient id and time
    event_log = event_log.sort_values(by=['case:concept:name', 'time:timestamp'])

    return event_log


if __name__ == '__main__':
    print('Extracting the event log ...')
    # Check if the event log already exists
    try:
        pd.read_csv(CLEAN_EVENT_LOG_PATH)
        print('The event log already exists. Skipping extraction.')
        exit(0)
    except FileNotFoundError:
        pass

    # Load the data
    path = f'{ROOT_DIR}/backend/data/raw/{RAW_DATASET}'
    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print(
            f'The ORCHID dataset was not found at {path}. Please download the dataset and place it in the data/raw '
            f'folder.')
        exit(1)

    event_log = extract(df)

    # Save the event log
    event_log.to_csv(CLEAN_EVENT_LOG_PATH, index=False)
