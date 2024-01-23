from backend.src.dataclasses.filters import CategoricalFilter, FilterOperator, NumericalFilter
from backend.src.process_mining.event_log import filter_log


class TestEventLogFiltering:
    def test_is_empty(self, test_log):
        filters = [CategoricalFilter(attribute_name='outcome_heart', operator=FilterOperator.IS_EMPTY, values=None)]

        el = filter_log(test_log, filters)

        assert len(el) == 2

    def test_is_not_empty(self, test_log):
        filters = [CategoricalFilter(attribute_name='outcome_heart', operator=FilterOperator.IS_NOT_EMPTY, values=None)]

        el = filter_log(test_log, filters)

        assert len(el) == 6

    def test_equals(self, test_log):
        filters = [CategoricalFilter(attribute_name='opo_id', operator=FilterOperator.EQUALS, values=['OPO2'])]

        el = filter_log(test_log, filters)

        assert len(el) == 2

    def test_not_equals(self, test_log):
        filters = [CategoricalFilter(attribute_name='opo_id', operator=FilterOperator.NOT_EQUALS, values=['OPO2'])]

        el = filter_log(test_log, filters)

        assert len(el) == 6

    def test_contains(self, test_log):
        filters = [CategoricalFilter(attribute_name='opo_id', operator=FilterOperator.CONTAINS, values=['OPO2'])]

        el = filter_log(test_log, filters)

        assert len(el) == 2

        filters = [
            CategoricalFilter(attribute_name='opo_id', operator=FilterOperator.CONTAINS, values=['OPO2', 'OPO1'])]

        el = filter_log(test_log, filters)

        assert len(el) == 8

    def test_not_contains(self, test_log):
        filters = [CategoricalFilter(attribute_name='opo_id', operator=FilterOperator.NOT_CONTAINS, values=['OPO2'])]

        el = filter_log(test_log, filters)

        assert len(el) == 6

        filters = [
            CategoricalFilter(attribute_name='opo_id', operator=FilterOperator.NOT_CONTAINS, values=['OPO2', 'OPO1'])]

        el = filter_log(test_log, filters)

        assert len(el) == 0

    def test_less_than(self, test_log):
        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.LESS_THAN, value=20)]

        el = filter_log(test_log, filters)

        assert len(el) == 2

        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.LESS_THAN, value=15)]

        el = filter_log(test_log, filters)

        assert len(el) == 0

    def test_less_than_or_equals(self, test_log):
        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.LESS_THAN_OR_EQUALS, value=15)]

        el = filter_log(test_log, filters)

        assert len(el) == 2

        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.LESS_THAN_OR_EQUALS, value=10)]

        el = filter_log(test_log, filters)

        assert len(el) == 0

    def test_greater_than(self, test_log):
        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.GREATER_THAN, value=20)]

        el = filter_log(test_log, filters)

        assert len(el) == 6

        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.GREATER_THAN, value=39)]

        el = filter_log(test_log, filters)

        assert len(el) == 0

    def test_greater_than_or_equals(self, test_log):
        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.GREATER_THAN_OR_EQUALS, value=20)]

        el = filter_log(test_log, filters)

        assert len(el) == 6

        filters = [NumericalFilter(attribute_name='age', operator=FilterOperator.GREATER_THAN_OR_EQUALS, value=39)]

        el = filter_log(test_log, filters)

        assert len(el) == 6
