import os

import pytest

from backend.src.dataclasses.attributes import DisaggregationAttribute, AttributeType
from backend.src.flask.services.process_mining_service import ProcessMiningService
from backend.src.process_mining.event_log import load_event_log, load_patient_attributes
from definitions import ROOT_DIR


@pytest.fixture(scope='module')
def test_process_mining_service():
    pms = ProcessMiningService()
    pms.event_log = load_event_log(os.path.join(ROOT_DIR, 'tests', 'test_sample.csv'))
    pms.patient_attributes = load_patient_attributes(pms.event_log)
    return pms


@pytest.fixture(scope='module')
def test_log(test_process_mining_service):
    return test_process_mining_service.event_log


@pytest.fixture(scope='session')
def process_mining_service():
    return ProcessMiningService()


@pytest.fixture(scope='session')
def patient_attributes(process_mining_service):
    return process_mining_service.get_patient_attributes()


@pytest.fixture(scope='session')
def event_log(process_mining_service):
    return process_mining_service.event_log


@pytest.fixture
def categorical_disaggregation_attribute():
    return DisaggregationAttribute(
        name='gender',
        type=AttributeType.CATEGORICAL)


@pytest.fixture
def numerical_disaggregation_attribute():
    return DisaggregationAttribute(
        name='age',
        type=AttributeType.NUMERICAL,
        bins=[0, 30, 60, 90])
