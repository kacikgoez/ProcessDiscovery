import pytest

from backend.src.dataclasses.attributes import CategoricalAttribute, NumericalAttribute
from backend.src.flask.services.process_mining_service import ProcessMiningService
from definitions import PATIENT_ATTRIBUTES


class TestPatientAttributes:
    @pytest.fixture(scope='class')
    def process_mining_service(self):
        return ProcessMiningService()

    @pytest.fixture(scope='class')
    def patient_attributes(self, process_mining_service):
        return process_mining_service.get_patient_attributes()

    def test_correct_types(self, patient_attributes):
        assert isinstance(patient_attributes, list)
        assert all(isinstance(attribute, (CategoricalAttribute, NumericalAttribute)) for attribute in patient_attributes)

    def test_all_attributes_exist(self, patient_attributes):
        for name, attribute_type in PATIENT_ATTRIBUTES.items():
            assert any(attribute.name == name for attribute in patient_attributes)
        assert len(patient_attributes) == len(PATIENT_ATTRIBUTES)

    def test_all_attributes_have_correct_type(self, patient_attributes):
        for name, attribute_type in PATIENT_ATTRIBUTES.items():
            assert any(attribute.name == name and attribute.type == attribute_type.value for attribute in patient_attributes)

    def test_all_numerical_attributes_have_default_groups(self, patient_attributes):
        for name, attribute_type in PATIENT_ATTRIBUTES.items():
            if attribute_type == 'numerical':
                assert any(attribute.name == name and len(attribute.groups) > 0 for attribute in patient_attributes)