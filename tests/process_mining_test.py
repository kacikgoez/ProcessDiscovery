import pytest
from backend.src.dataclasses.attributes import DisaggregationAttribute, AttributeType
from backend.src.dataclasses.charts import DataSeries, MultiDataSeries, DataItem, Graph, Node, Edge, Variant
from backend.src.dataclasses.requests import KpiRequest, KpiType, DistributionRequest, VariantListRequest, DfgRequest
from backend.src.process_mining.variants import get_variants_with_case_ids


class TestDistribution:
    def test_categorical_distribution(self, test_process_mining_service, categorical_disaggregation_attribute):
        request = DistributionRequest(
            filters=[],
            disaggregation_attribute=categorical_disaggregation_attribute)

        result = test_process_mining_service.get_attribute_distribution(request)

        expected = DataSeries.from_dict(data={
            'F': 1,
            'M': 1
        }, name='gender')

        assert result == expected

    def test_numerical_distribution(self, test_process_mining_service, numerical_disaggregation_attribute):
        request = DistributionRequest(
            filters=[],
            disaggregation_attribute=numerical_disaggregation_attribute)

        result = test_process_mining_service.get_attribute_distribution(request)

        expected = DataSeries.from_dict(data={
            '0 - 30': 1,
            '30 - 60': 1,
            '60 - 90': 0
        }, name='age')

        assert result == expected


class TestVariants:
    def test_get_variants_with_case_ids(self, test_log):
        variants = get_variants_with_case_ids(test_log)

        expected = {
            ('Referral', 'Evaluation'): ['OPO2_P1000'],
            ('Referral', 'Evaluation', 'Approach', 'Authorization', 'Procurement', 'Transplant'): ['OPO1_P102650'],
        }

        assert variants == expected

    def test_variants(self, test_process_mining_service, categorical_disaggregation_attribute):
        request = VariantListRequest(
            filters=[],
            disaggregation_attribute=categorical_disaggregation_attribute)

        result = test_process_mining_service.get_variants(request)

        expected = [
            Variant(
                activities=['Referral', 'Evaluation', 'Approach', 'Authorization', 'Procurement', 'Transplant'],
                count=1, frequency=0.5,
                distribution=DataSeries.from_dict(data={'F': 1, 'M': 0}, name='gender')),
            Variant(
                activities=['Referral', 'Evaluation'],
                count=1, frequency=0.5,
                distribution=DataSeries.from_dict(data={'M': 1, 'F': 0}, name='gender')),
        ]

        assert result == expected


class TestKPI:
    @pytest.fixture
    def happy_request(self):
        return KpiRequest(
            filters=[],
            kpi=KpiType.HAPPY_PATH_ADHERENCE,
            disaggregation_attribute=DisaggregationAttribute('gender', AttributeType.CATEGORICAL),
            legend_attribute=DisaggregationAttribute('referral_year', AttributeType.CATEGORICAL))

    @pytest.fixture
    def drop_request(self):
        return KpiRequest(
            filters=[],
            kpi=KpiType.DROP_OUT,
            disaggregation_attribute=DisaggregationAttribute('referral_year', AttributeType.CATEGORICAL))

    @pytest.fixture
    def permuted_request(self):
        return KpiRequest(
            filters=[],
            kpi=KpiType.PERMUTED_PATH_ADHERENCE,
            disaggregation_attribute=DisaggregationAttribute('brain_death', AttributeType.CATEGORICAL),
            legend_attribute=DisaggregationAttribute('race', AttributeType.CATEGORICAL))

    @pytest.fixture
    def bureaucratic_request(self):
        return KpiRequest(
            filters=[],
            kpi=KpiType.BUREAUCRATIC_DURATION,
            disaggregation_attribute=DisaggregationAttribute('gender', AttributeType.CATEGORICAL),
            legend_attribute=DisaggregationAttribute('cause_of_death', AttributeType.CATEGORICAL))

    @pytest.fixture
    def eva_request(self):
        return KpiRequest(
            filters=[],
            kpi=KpiType.EVALUATION_TO_APPROACH,
            disaggregation_attribute=DisaggregationAttribute('gender', AttributeType.CATEGORICAL),
            legend_attribute=DisaggregationAttribute('circumstances_of_death', AttributeType.CATEGORICAL))

    @pytest.fixture
    def aut_request(self):
        return KpiRequest(
            filters=[],
            kpi=KpiType.AUTHORIZATION_TO_PROCUREMENT,
            disaggregation_attribute=DisaggregationAttribute('gender', AttributeType.CATEGORICAL),
            legend_attribute=DisaggregationAttribute('opo_id', AttributeType.CATEGORICAL))

    def test_happypath(self, test_process_mining_service, happy_request):
        expected = MultiDataSeries(name='Happy path adherence', series=[
            DataSeries(name='2018', data=[
                DataItem(x='F', y=0.0),
                DataItem(x='M', y=0.0)]),
            DataSeries(name='2019', data=[
                DataItem(x='F', y=1.0),
                DataItem(x='M', y=0.0)])])

        result = test_process_mining_service.get_kpi_data(happy_request)

        assert result == expected

    def test_drop(self, test_process_mining_service, drop_request):
        expected = MultiDataSeries(name='Dropout rate', series=[
            DataSeries(name='2018', data=[
                DataItem(x='Evaluation', y=1.0),
                DataItem(x='Transplant', y=0.0)]),
            DataSeries(name='2019', data=[
                DataItem(x='Evaluation', y=0.0),
                DataItem(x='Transplant', y=1.0)])])

        result = test_process_mining_service.get_kpi_data(drop_request)

        assert result == expected

    def test_permuted(self, test_process_mining_service, permuted_request):
        expected = MultiDataSeries(name='Permuted path adherence', series=[
            DataSeries(name='Hispanic', data=[
                DataItem(x=False, y=1.0)])])

        result = test_process_mining_service.get_kpi_data(permuted_request)

        assert result == expected

    def test_bureaucratic(self, test_process_mining_service, bureaucratic_request):
        expected = MultiDataSeries(name='Bureaucratic duration', series=[
            DataSeries(name='Head Trauma', data=[
                DataItem(x='F', y=240.0),  # 4 minutes
                DataItem(x='M', y=0.0)
            ])])

        result = test_process_mining_service.get_kpi_data(bureaucratic_request)

        assert result == expected

    def test_eva(self, test_process_mining_service, eva_request):
        expected = MultiDataSeries(name='Evaluation to approach', series=[
            DataSeries(name='Accident, Non-MVA', data=[
                DataItem(x='F', y=0.0),
                DataItem(x='M', y=0.0)
            ]),
            DataSeries(name='MVA', data=[
                DataItem(x='F', y=60.0),
                DataItem(x='M', y=0.0)
            ])
        ])

        result = test_process_mining_service.get_kpi_data(eva_request)

        assert result == expected

    def test_aut(self, test_process_mining_service, aut_request):
        expected = MultiDataSeries(name='Authorization to procurement', series=[
            DataSeries(name='OPO1', data=[
                DataItem(x='F', y=60.0),
                DataItem(x='M', y=0.0)
            ]),
            DataSeries(name='OPO2', data=[
                DataItem(x='F', y=0.0),
                DataItem(x='M', y=0.0)
            ]),
        ])

        result = test_process_mining_service.get_kpi_data(aut_request)

        assert result == expected


class TestDFG:
    @pytest.fixture
    def dfg_request(self, categorical_disaggregation_attribute):
        return DfgRequest(
            filters=[],
            disaggregation_attribute=categorical_disaggregation_attribute,
        )

    def test_dfg(self, test_process_mining_service, dfg_request):
        result = test_process_mining_service.get_dfg(dfg_request)

        expected = Graph(
            name='DFG',
            nodes=[
                Node(id='Referral', label='Referral', value=None),
                Node(id='Evaluation', label='Evaluation', value=None),
                Node(id='Approach', label='Approach', value=None),
                Node(id='Authorization', label='Authorization', value=None),
                Node(id='Procurement', label='Procurement', value=None),
                Node(id='Transplant', label='Transplant', value=None),
            ],
            edges=[
                Edge(source='Referral', target='Evaluation', label=None, value=2),
                Edge(source='Evaluation', target='Approach', label=None, value=1),
                Edge(source='Approach', target='Authorization', label=None, value=1),
                Edge(source='Authorization', target='Procurement', label=None, value=1),
                Edge(source='Procurement', target='Transplant', label=None, value=1),
            ]
        )

        # compare the nodes without order
        assert sorted(result.nodes, key=lambda node: node.id) == sorted(expected.nodes, key=lambda node: node.id)

        # compare the edges without order
        assert sorted(result.edges, key=lambda edge: (edge.source, edge.target)) == sorted(expected.edges, key=lambda edge: (edge.source, edge.target))
