from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CopyChartTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create("my chart", "BOOTHS")

        copied_chart = self.client.charts.copy(chart.key)

        assert_that(copied_chart.name).is_equal_to("my chart (copy)")
