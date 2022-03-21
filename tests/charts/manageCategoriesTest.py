from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class UpdateChartTest(SeatsioClientTest):

    def test_add_category(self):
        category1 = {"key": 1, "label": "Category 1", "color": "#aaaaaa", "accessible": False}
        chart = self.client.charts.create(name="aChart", categories=[category1])

        category_to_add = {"key": 2, "label": "Category 2", "color": "#bbbbbb", "accessible": True}
        self.client.charts.add_category(chart.key, category_to_add)

        retrieved_chart = self.client.charts.retrieve(chart.key)
        drawing = self.client.charts.retrieve_published_version(retrieved_chart.key)
        assert_that(drawing.categories.list).contains_exactly(category1, category_to_add)

    def test_remove_category(self):
        category1 = {"key": 1, "label": "Category 1", "color": "#aaaaaa", "accessible": False}
        category2 = {"key": "cat2", "label": "Category 2", "color": "#bbbbbb", "accessible": True}
        chart = self.client.charts.create(name="aChart", categories=[category1, category2])

        self.client.charts.remove_category(chart.key, 1)
        self.client.charts.remove_category(chart.key, "cat2")

        retrieved_chart = self.client.charts.retrieve(chart.key)
        drawing = self.client.charts.retrieve_published_version(retrieved_chart.key)
        assert_that(drawing.categories.list).is_empty()


