from seatsio.domain import Chart
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CreateChartTest(SeatsioClientTest):

    def testDefaultParameters(self):
        chart = self.client.charts.create()

        assert_that(chart).is_instance(Chart)
        assert_that(chart.id).is_not_zero()
        assert_that(chart.key).is_not_blank()
        assert_that(chart.status).is_equal_to("NOT_USED")
        assert_that(chart.name).is_equal_to("Untitled chart")
        assert_that(chart.published_version_thumbnail_url).is_not_blank()
        assert_that(chart.draft_version_thumbnail_url).is_none()
        assert_that(chart.events).is_none()
        assert_that(chart.tags).is_empty()
        assert_that(chart.archived).is_false()

        drawing = self.client.charts.retrieve_published_version(chart.key)
        assert_that(drawing.venueType).is_equal_to("SIMPLE")
        assert_that(drawing.categories.list).is_empty()

    def testName(self):
        chart = self.client.charts.create(name="aChart")

        assert_that(chart.name).is_equal_to("aChart")
        drawing = self.client.charts.retrieve_published_version(chart.key)
        assert_that(drawing.venueType).is_equal_to("SIMPLE")
        assert_that(drawing.categories.list).is_empty()

    def testVenueType(self):
        chart = self.client.charts.create(venue_type="SIMPLE")

        assert_that(chart.name).is_equal_to("Untitled chart")
        drawing = self.client.charts.retrieve_published_version(chart.key)
        assert_that(drawing.venueType).is_equal_to("SIMPLE")
        assert_that(drawing.categories.list).is_empty()

    def testCategories(self):
        chart = self.client.charts.create(
            categories=[
                {"key": 1, "label": "Category 1", "color": "#aaaaaa"},
                {"key": 2, "label": "Category 2", "color": "#bbbbbb", "accessible": True}
            ])

        assert_that(chart.name).is_equal_to("Untitled chart")
        drawing = self.client.charts.retrieve_published_version(chart.key)
        assert_that(drawing.venueType).is_equal_to("SIMPLE")
        assert_that(drawing.categories.list).contains_exactly_in_any_order(
            {"key": 1, "label": "Category 1", "color": "#aaaaaa", "accessible": False},
            {"key": 2, "label": "Category 2", "color": "#bbbbbb", "accessible": True}
        )
