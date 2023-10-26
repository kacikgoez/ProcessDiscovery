import pandas as pd
from pandas import Timedelta

from app import ROOT_DIR, CLEAN_EVENT_LOG_PATH

"""
This script is used to extract an event log from the original data.
We use the Organ Retrieval and Collection of Health Information for Donation (ORCHID) dataset https://doi.org/10.13026/eytj-4f29.
As the dataset is not publicly available, we cannot provide the data here.
You can request access to the data and place the `opd.csv` file in the `data/raw` folder.

Author: Hannes Drescher
"""

RAW_DATASET = 'opd.csv'

PATIENT_DATA_MAPPING = {
    'PatientID': 'case:concept:name',  # The case id
    'OPO': 'opo_id',
    'HospitalID': 'hospital_id',
    'Age': 'age',
    'Gender': 'gender',
    'Race': 'race',
    'brain_death': 'brain_death',
    'Referral_Year': 'referral_year',  # interesting as the time attributes are randomly shifted
    'Referral_DayOfWeek': 'referral_day_of_week',  # interesting as the time attributes are randomly shifted
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
"""
The mapping is used to map the original column names to the column names used in the event log.
The keys are the original column names and the values are the new column names.
"""

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
        f'The ORCHID dataset was not found at {path}. Please download the dataset and place it in the data/raw folder.')
    exit(1)

# Convert all time columns to datetime
time_columns = ['time_referred', 'time_approached', 'time_authorized', 'time_procured']
for col in time_columns:
    df[col] = pd.to_datetime(df[col], format='ISO8601')

# Only keep allowed outcomes
allowed_outcomes = ['Transplanted', 'Recovered for Research', 'Recovered for Transplant but not Transplanted']
include_outcomes = [c for c in PATIENT_DATA_MAPPING.keys() if c.startswith('outcome_')]
for col in include_outcomes:
    df[col] = df[col].astype('category').cat.set_categories(allowed_outcomes)

events_list = []
# Iterate over all rows that correspond to a patient and add all events that happened to the patient to the event list
for i, row in df.iterrows():
    # Collect patient data by mapping the original column names to the new column names
    patient_data = {v: row[k] for k, v in PATIENT_DATA_MAPPING.items()}

    # Add the referral and evaluation events for each patient as all patients were referred and evaluated
    events_list.append({'concept:name': 'Referral', 'time:timestamp': row['time_referred']} | patient_data)

    # Unfortunately, the evaluation time is not available in the dataset
    # We assume that the evaluation happens one minute after the referral
    events_list.append(
        {'concept:name': 'Evaluation', 'time:timestamp': row['time_referred'] + Timedelta(minutes=1)} | patient_data)

    # Add each activity only if its corresponding entry is not False
    if row['approached']:
        events_list.append({'concept:name': 'Approach', 'time:timestamp': row['time_approached']} | patient_data)

    if row['authorized']:
        events_list.append({'concept:name': 'Authorization', 'time:timestamp': row['time_authorized']} | patient_data)

    if row['procured']:
        events_list.append({'concept:name': 'Procurement', 'time:timestamp': row['time_procured']} | patient_data)

    # Unfortunately, the transplant time is not available in the dataset
    # We assume that the transplant happens one minute after the procurement
    if row['transplanted']:
        events_list.append({'concept:name': 'Transplant',
                            'time:timestamp': row['time_procured'] + Timedelta(minutes=1)} | patient_data)

# Transform the event list to a dataframe
columns = ['concept:name', 'time:timestamp'] + list(PATIENT_DATA_MAPPING.values())
event_log = pd.DataFrame(events_list, columns=columns)

# Forward fill the time column to fill in the missing times
event_log['time:timestamp'] = event_log['time:timestamp'].ffill()

# Sort the event log by patient id and time
event_log = event_log.sort_values(by=['case:concept:name', 'time:timestamp'])

# Save the event log
event_log.to_csv(CLEAN_EVENT_LOG_PATH, index=False)
