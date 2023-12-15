import pytest

from backend.src.dataclasses.attributes import DisaggregationAttribute, AttributeType
from backend.src.flask.services.process_mining_service import ProcessMiningService
from backend.src.process_mining.event_log import create_bins


class TestPatientAttributes:
    @pytest.fixture
    def process_mining_service(self):
        return ProcessMiningService()

    @pytest.fixture
    def event_log(self, process_mining_service):
        return process_mining_service.event_log

    @pytest.fixture
    def categorical_disaggregation_attribute(self):
        return DisaggregationAttribute(
            name='gender',
            type=AttributeType.CATEGORICAL)

    @pytest.fixture
    def numerical_disaggregation_attribute(self):
        return DisaggregationAttribute(
            name='age',
            type=AttributeType.NUMERICAL,
            bins=[0, 30, 60, 90])

    def test_bins_only_for_numerical_attributes(self, categorical_disaggregation_attribute):
        with pytest.raises(ValueError):
            categorical_disaggregation_attribute.get_bins()

    def test_bin_labels_only_for_numerical_attributes(self, categorical_disaggregation_attribute):
        with pytest.raises(ValueError):
            categorical_disaggregation_attribute.get_bin_labels()

    def test_correct_bins_without_infinities(self, numerical_disaggregation_attribute):
        assert numerical_disaggregation_attribute.get_bins() == [0, 30, 60, 90]

    def test_correct_bins_with_infinities(self, numerical_disaggregation_attribute):
        assert numerical_disaggregation_attribute.get_bins(include_infinities=True) == [
            -float('inf'), 0, 30, 60, 90, float('inf')]

    def test_correct_bin_labels_without_infinities(self, numerical_disaggregation_attribute):
        assert numerical_disaggregation_attribute.get_bin_labels() == [
            '0 - 30',
            '30 - 60',
            '60 - 90',
        ]

    def test_correct_bin_labels_with_infinities(self, numerical_disaggregation_attribute):
        assert numerical_disaggregation_attribute.get_bin_labels(include_infinities=True) == [
            '< 0',
            '0 - 30',
            '30 - 60',
            '60 - 90',
            '> 90',
        ]

    def test_binning_without_disaggregation_attribute(self, event_log):
        assert event_log.equals(create_bins(event_log))

    def test_binning_for_categorical_attribute(self, event_log, categorical_disaggregation_attribute):
        el = create_bins(event_log, categorical_disaggregation_attribute)

        # original event log should not be modified
        assert el[categorical_disaggregation_attribute.name].equals(event_log[categorical_disaggregation_attribute.name])
        # new column should be added
        assert 'temp' in el.columns
        # new column should be equal to the original column
        assert el['temp'].equals(el[categorical_disaggregation_attribute.name])

    def test_binning_for_numerical_attribute(self, event_log, numerical_disaggregation_attribute):
        el = create_bins(event_log, numerical_disaggregation_attribute)

        # original event log should not be modified
        assert el[numerical_disaggregation_attribute.name].equals(event_log[numerical_disaggregation_attribute.name])
        # new column should be added
        assert 'temp' in el.columns

        # new column should only contain the bin labels or NaN (if the value does not fit into any bin)
        assert el['temp'].dropna().isin(numerical_disaggregation_attribute.get_bin_labels()).all()
