from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListChartsInArchiveTest(SeatsioClientTest):

    def test(self):
        chart1 = self.client.charts.create()
        chart2 = self.client.charts.create()
        chart3 = self.client.charts.create()

        self.client.charts.move_to_archive(chart1.key)
        self.client.charts.move_to_archive(chart3.key)

        charts = self.client.charts.archive.list()

        assert_that(charts).extracting("key").contains_exactly(chart3.key, chart1.key)
