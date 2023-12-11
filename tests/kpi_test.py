import pytest
from backend.src.dataclasses import AttributeType, DisaggregationAttribute,\
    KpiRequest, KpiType
from backend.src.process_mining.event_log import load_event_log, load_patient_attributes
from backend.src.flask.services.process_mining_service import ProcessMiningService



def process_mining_service():
    process = ProcessMiningService()
    process.event_log = load_event_log('test_sample.csv')
    process.patient_attributes = load_patient_attributes(process.event_log)
    return process


class TestKPI:
    @pytest.fixture
    def happy_request(self):
        return KpiRequest(KpiType.HAPPY_PATH_ADHERENCE, DisaggregationAttribute('gender',AttributeType.CATEGORICAL),
                          DisaggregationAttribute('referral_year',AttributeType.CATEGORICAL))

    @pytest.fixture
    def drop_request(self):
        return KpiRequest(KpiType.DROP_OUT, DisaggregationAttribute('age',AttributeType.NUMERICAL, [0, 20, 40]))

    @pytest.fixture
    def permuted_request(self):
        return KpiRequest(KpiType.PERMUTED_PATH_ADHERENCE, DisaggregationAttribute('brain_death', AttributeType.CATEGORICAL),
                          DisaggregationAttribute('race', AttributeType.CATEGORICAL))

    @pytest.fixture
    def bureaucratic_request(self):
        return KpiRequest(KpiType.BUREAUCRATIC_DURATION,
                          DisaggregationAttribute('cause_of_death', AttributeType.CATEGORICAL),
                          DisaggregationAttribute('gender', AttributeType.CATEGORICAL))

    @pytest.fixture
    def eva_request(self):
        return KpiRequest(KpiType.EVALUATION_TO_APPROACH,
                          DisaggregationAttribute('circumstances_of_death', AttributeType.CATEGORICAL),
                          DisaggregationAttribute('gender', AttributeType.CATEGORICAL))

    @pytest.fixture
    def aut_request(self):
        return KpiRequest(KpiType.AUTHORIZATION_TO_PROCUREMENT,
                          DisaggregationAttribute('gender', AttributeType.CATEGORICAL),
                          DisaggregationAttribute('opo_id', AttributeType.CATEGORICAL))

    @pytest.fixture
    def permuted_dfg_request(self):
        return KpiRequest(KpiType.PERMUTED_PATH_DFG)

    def test_happypath(self, happy_request):
        assert process_mining_service().get_kpi_data(happy_request) == {'axis': [2018, 2019],'legend': ['F', 'M'],
                                                                        'value': {'F': [0.0, 1.0], 'M': [0.0, 0.0]}}

    def test_drop(self,  drop_request):
        assert process_mining_service().get_kpi_data(drop_request) == {'axis': ['Evaluation', 'Transplant'],
                                                                        'legend': ['0 - 20', '0 - 20_percentage',
                                                                                   '20 - 40', '20 - 40_percentage'],
                                                                        'value': {'0 - 20': [1.0, 0.0],
                                                                                  '0 - 20_percentage': [0.5, 0.0],
                                                                                  '20 - 40': [0.0, 1.0],
                                                                                  '20 - 40_percentage': [0.0, 0.5]}}

    def test_permuted(self,  permuted_request):
        assert process_mining_service().get_kpi_data(permuted_request) == {'axis': ['Hispanic'],
                                                                           'legend': ['total_cases', False],
                                                                           'value': {False: [1], 'total_cases': [1, 1]}}
    def test_bureaucratic(self, bureaucratic_request):
        assert process_mining_service().get_kpi_data(bureaucratic_request) == {'legend': ['Head Trauma'],
                                                                                'value': {'Head Trauma': [['F', 4]]}}

    def test_eva(self,  eva_request):
        assert process_mining_service().get_kpi_data( eva_request)['value']['MVA'] == [['F', 1]]

    def test_aut(self, aut_request):
        assert process_mining_service().get_kpi_data(aut_request)['value'] == {'F': [['OPO1', 1]], 'M': []}

    def test_permuted_dfg(self,  permuted_dfg_request):
        assert process_mining_service().get_kpi_data(permuted_dfg_request)['links'] == [{'absolute_frequency': 1,\
                                          'source': 'Approach', 'target': 'Authorization'},
                                         {'absolute_frequency': 1, 'source': 'Authorization', 'target': 'Procurement'},
                                         {'absolute_frequency': 1, 'source': 'Evaluation', 'target': 'Approach'},
                                         {'absolute_frequency': 1, 'source': 'Procurement', 'target': 'Transplant'},
                                         {'absolute_frequency': 2, 'source': 'Referral', 'target': 'Evaluation'}]






