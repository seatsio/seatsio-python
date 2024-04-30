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

    def test_list_categories(self):
        category1 = {"key": 1, "label": "Category 1", "color": "#aaaaaa", "accessible": False}
        category2 = {"key": "cat2", "label": "Category 2", "color": "#bbbbbb", "accessible": True}
        chart = self.client.charts.create(name="aChart", categories=[category1, category2])

        category_list = self.client.charts.list_categories(chart.key)
        assert_that(category_list[0].key).is_equal_to(category1["key"])
        assert_that(category_list[1].key).is_equal_to(category2["key"])

    def test_update_category(self):
        category1 = {"key": 1, "label": "Category 1", "color": "#aaaaaa", "accessible": False}
        chart = self.client.charts.create(name="aChart", categories=[category1])

        self.client.charts.update_category(chart_key=chart.key, category_key=1, label="Updated label", color="#bbbbbb", accessible=True)

        category_list = self.client.charts.list_categories(chart.key)
        assert_that(category_list[0].label).is_equal_to("Updated label")
        assert_that(category_list[0].color).is_equal_to("#bbbbbb")
        assert_that(category_list[0].accessible).is_true()