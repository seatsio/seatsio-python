from seatsio.exceptions import SeatsioException
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class UpdateChartTest(SeatsioClientTest):

    def test_update_name(self):
        category = {"key": 1, "label": "Category 1", "color": "#aaaaaa", "accessible": False}
        chart = self.client.charts.create(venue_type="SIMPLE", categories=[category])

        self.client.charts.update(chart.key, new_name="aChart")

        retrieved_chart = self.client.charts.retrieve(chart.key)
        assert_that(retrieved_chart.name).is_equal_to("aChart")
        drawing = self.client.charts.retrieve_published_version(retrieved_chart.key)
        assert_that(drawing.venueType).is_equal_to("SIMPLE")
        assert_that(drawing.categories.list).contains_exactly(category)

    def test_update_categories(self):
        chart = self.client.charts.create(name="aChart - unchanged", venue_type="SIMPLE", categories=[])
        category1 = {"key": 1, "label": "Category 1", "color": "#aaaaaa", "accessible": False}
        category2 = {"key": 2, "label": "Category 2", "color": "#bbbbbb", "accessible": True}

        self.client.charts.update(chart.key, categories=[category1, category2])

        retrieved_chart = self.client.charts.retrieve(chart.key)
        assert_that(retrieved_chart.name).is_equal_to("aChart - unchanged")
        drawing = self.client.charts.retrieve_published_version(retrieved_chart.key)
        assert_that(drawing.venueType).is_equal_to("SIMPLE")
        assert_that(drawing.categories.list).contains_exactly(category1, category2)

    def test_update_categories_post_garbage(self):
        chart = self.client.charts.create(name="aChart - unchanged", venue_type="SIMPLE", categories=[])
        category = "sdkqlmqdsklmsdq"

        try:
            self.client.charts.update(chart.key, categories=[category])
            self.fail("expected an exception")
        except SeatsioException as e:
            assert_that(e.message).is_equal_to("#/categories/0: expected type: JSONObject, found: String.")
            assert_that(e.requestId).is_not_none()
            assert_that(e.cause).is_none()
