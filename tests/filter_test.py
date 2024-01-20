import os

import pytest

from backend.src.dataclasses.filters import CategoricalFilter, FilterOperator, NumericalFilter
from backend.src.flask.services.process_mining_service import ProcessMiningService
from backend.src.process_mining.event_log import load_event_log, load_patient_attributes, filter_log
from definitions import ROOT_DIR


class TestEventLogFiltering:
    @pytest.fixture
    def process_mining_service(self):
        pms = ProcessMiningService()
        pms.event_log = load_event_log(os.path.join(ROOT_DIR, 'tests', 'test_sample.csv'))
        pms.patient_attributes = load_patient_attributes(pms.event_log)
        return pms

    @pytest.fixture
    def event_log(self, process_mining_service):
        return process_mining_service.event_log

    def test_is_empty(self, event_log):
        filters = [CategoricalFilter(attribute_name='outcome_heart', operator=FilterOperator.IS_EMPTY, values=None)]

        el = filter_log(event_log, filters)

        assert len(el) == 2

    def test_is_not_empty(self, event_log):
        filters = [CategoricalFilter(attribute_name='outcome_heart', operator=FilterOperator.IS_NOT_EMPTY, values=None)]

        el = filter_log(event_log, filters)

        assert len(el) == 6

    def test_equals(self, event_log):
        filters = [CategoricalFilter(attribute_name='opo_id', operator=FilterOperator.EQUALS, values=['OPO2'])]

        el = filter_log(event_log, filters)

        assert len(el) == 2

    def test_not_equals(self, event_log):
        filters = [CategoricalFilter(attribute_name='opo_id', operator=FilterOperator.NOT_EQUALS, values=['OPO2'])]

        el = filter_log(event_log, filters)

        assert len(el) == 6

    def test_contains(self, event_log):
        filters = [CategoricalFilter(attribute_name='opo_id', operator=FilterOperator.CONTAINS, values=['OPO2'])]

        el = filter_log(event_log, filters)

        assert len(el) == 2

        filters = [CategoricalFilter(attribute_name='opo_id', operator=FilterOperator.CONTAINS, values=['OPO2', 'OPO1'])]

        el = filter_log(event_log, filters)

        assert len(el) == 8

    def test_not_contains(self, event_log):
        filters = [CategoricalFilter(attribute_name='opo_id', operator=FilterOperator.NOT_CONTAINS, values=['OPO2'])]

        el = filter_log(event_log, filters)

        assert len(el) == 6

        filters = [CategoricalFilter(attribute_name='opo_id', operator=FilterOperator.NOT_CONTAINS, values=['OPO2', 'OPO1'])]

        el = filter_log(event_log, filters)

        assert len(el) == 0

    def test_less_than(self, event_log):
        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.LESS_THAN, value=20)]

        el = filter_log(event_log, filters)

        assert len(el) == 2

        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.LESS_THAN, value=15)]

        el = filter_log(event_log, filters)

        assert len(el) == 0

    def test_less_than_or_equals(self, event_log):
        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.LESS_THAN_OR_EQUALS, value=15)]

        el = filter_log(event_log, filters)

        assert len(el) == 2

        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.LESS_THAN_OR_EQUALS, value=10)]

        el = filter_log(event_log, filters)

        assert len(el) == 0

    def test_greater_than(self, event_log):
        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.GREATER_THAN, value=20)]

        el = filter_log(event_log, filters)

        assert len(el) == 6

        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.GREATER_THAN, value=39)]

        el = filter_log(event_log, filters)

        assert len(el) == 0

    def test_greater_than_or_equals(self, event_log):
        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.GREATER_THAN_OR_EQUALS, value=20)]

        el = filter_log(event_log, filters)

        assert len(el) == 6

        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.GREATER_THAN_OR_EQUALS, value=39)]

        el = filter_log(event_log, filters)

        assert len(el) == 6