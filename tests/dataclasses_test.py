import pandas as pd
import pytest

from backend.src.dataclasses.charts import DataSeries, DataItem, MultiDataSeries, Graph, Node, Edge


class TestChartDataclasses:
    def test_data_series_from_dict(self):
        data = {
            '0 - 30': 1,
            '30 - 60': 1,
            '60 - 90': 0
        }
        expected = DataSeries(name='age', data=[
            DataItem(x='0 - 30', y=1),
            DataItem(x='30 - 60', y=1),
            DataItem(x='60 - 90', y=0)])

        result = DataSeries.from_dict(name='age', data=data)

        assert result == expected

    def test_data_series_from_dict_sorted(self):
        data = {
            '60 - 90': 0,
            '0 - 30': 1,
            '30 - 60': 1,
        }
        expected = DataSeries(name='age', data=[
            DataItem(x='0 - 30', y=1),
            DataItem(x='30 - 60', y=1),
            DataItem(x='60 - 90', y=0)])

        result = DataSeries.from_dict(name='age', data=data)

        assert result == expected

    def test_data_series_from_dict_sorted_by_custom_order(self):
        data = {
            'Monday': 0,
            'Wednesday': 2,
            'Tuesday': 1,
        }
        expected = DataSeries(name='test', data=[
            DataItem(x='Monday', y=0),
            DataItem(x='Tuesday', y=1),
            DataItem(x='Wednesday', y=2)])

        result = DataSeries.from_dict(name='test', data=data, sort_by='referral_day_of_week')

        assert result == expected

    def test_multi_data_series_from_pandas(self):
        data = {
            '0 - 30': 1,
            '60 - 90': 0,
            '30 - 60': 2,
        }
        df = pd.Series(data=data, name='age')

        expected = MultiDataSeries(name='age', series=[
            DataSeries(name='age', data=[
                DataItem(x='0 - 30', y=1),
                DataItem(x='30 - 60', y=2),
                DataItem(x='60 - 90', y=0)])])

        result = MultiDataSeries.from_pandas(df=df, name='age')

        assert result == expected

    def test_multi_data_series_from_pandas_with_two_levels(self):
        data = [
            {
                'age': '0 - 30',
                'gender': 'F',
                'count': 1
            },
            {
                'age': '0 - 30',
                'gender': 'M',
                'count': 2
            },
            {
                'age': '30 - 60',
                'gender': 'F',
                'count': 3
            },
            {
                'age': '30 - 60',
                'gender': 'M',
                'count': 4
            },
        ]
        df = pd.DataFrame(data=data).groupby(['age', 'gender']).sum()['count']

        expected = MultiDataSeries(name='age', series=[
            DataSeries(name='0 - 30', data=[
                DataItem(x='F', y=1),
                DataItem(x='M', y=2)]),
            DataSeries(name='30 - 60', data=[
                DataItem(x='F', y=3),
                DataItem(x='M', y=4)])])

        result = MultiDataSeries.from_pandas(df=df, name='age')

        assert result == expected

    def test_multi_data_series_from_pandas_with_two_levels_sorted(self):
        data = [
            {
                'age': '30 - 60',
                'gender': 'M',
                'count': 4
            },
            {
                'age': '30 - 60',
                'gender': 'F',
                'count': 3
            },
            {
                'age': '0 - 30',
                'gender': 'F',
                'count': 1
            },
            {
                'age': '0 - 30',
                'gender': 'M',
                'count': 2
            },
        ]
        df = pd.DataFrame(data=data).groupby(['age', 'gender']).sum()['count']

        expected = MultiDataSeries(name='age', series=[
            DataSeries(name='0 - 30', data=[
                DataItem(x='F', y=1),
                DataItem(x='M', y=2)]),
            DataSeries(name='30 - 60', data=[
                DataItem(x='F', y=3),
                DataItem(x='M', y=4)])])

        result = MultiDataSeries.from_pandas(df=df, name='age')

        assert result == expected

    def test_graph_unique_node_ids(self):
        with pytest.raises(ValueError):
            Graph(
                name='test',
                nodes=[
                    Node(id='1', label='1'),
                    Node(id='1', label='1'),
                    Node(id='2', label='2'),
                ],
                edges=[]
            )

    def test_graph_invalid_edge(self):
        with pytest.raises(ValueError):
            Graph(
                name='test',
                nodes=[
                    Node(id='1', label='1'),
                    Node(id='2', label='2'),
                ],
                edges=[
                    Edge(source='1', target='3'),
                ]
            )
