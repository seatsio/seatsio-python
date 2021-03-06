from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class MoveChartOutOfArchiveTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create()
        self.client.charts.move_to_archive(chart.key)

        self.client.charts.move_out_of_archive(chart.key)

        retrieved_chart = self.client.charts.retrieve(chart.key)

        assert_that(retrieved_chart.archived).is_false()
