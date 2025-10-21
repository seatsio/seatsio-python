from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that

class MoveEventToNewChartCopyTest(SeatsioClientTest):

    def test_event_is_moved_to_new_chart_copy(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        moved_event = self.client.events.move_event_to_new_chart_copy(event.key)

        assert_that(moved_event.chart_key).is_not_equal_to(event.chart_key)
        assert_that(moved_event.key).is_equal_to(event.key)
