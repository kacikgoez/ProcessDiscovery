import pytest

from backend.src.dataclasses.attributes import DisaggregationAttribute, AttributeType
from backend.src.flask.services.process_mining_service import ProcessMiningService
from backend.src.process_mining.event_log import create_bins


class TestPatientAttributes:
    @pytest.fixture(scope='class')
    def process_mining_service(self):
        return ProcessMiningService()

    @pytest.fixture(scope='class')
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
        el, _ = create_bins(event_log)
        assert event_log.equals(el)

    def test_binning_for_categorical_attribute(self, event_log, categorical_disaggregation_attribute):
        original_event_log = event_log.copy()

        el, column = create_bins(event_log, categorical_disaggregation_attribute)

        # original event log should not be modified
        assert event_log.equals(original_event_log)

        # as the disaggregation attribute is categorical, the event log should not be modified at all
        assert event_log.equals(el)

    def test_binning_for_numerical_attribute(self, event_log, numerical_disaggregation_attribute):
        original_event_log = event_log.copy()

        el, column = create_bins(event_log, numerical_disaggregation_attribute)

        # original event log should not be modified
        assert event_log.equals(original_event_log)

        # new column should only contain the bin labels or NaN (if the value does not fit into any bin)
        assert el[column].isin(numerical_disaggregation_attribute.get_bin_labels() + [None]).all()
