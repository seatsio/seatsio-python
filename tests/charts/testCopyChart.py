from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CopyChartTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create("my chart", "SIMPLE")

        copied_chart = self.client.charts.copy(chart.key)

        assert_that(copied_chart.name).is_equal_to("my chart (copy)")
        drawing = self.client.charts.retrieve_published_version(copied_chart.key)
        assert_that(drawing.venueType).is_equal_to("SIMPLE")
