import time

from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListEventLogItems(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create()
        self.client.charts.update(chart.key, 'a chart')

        time.sleep(2)

        event_log_items = self.client.event_log.list()

        assert_that(event_log_items).extracting("type").contains_exactly("chart.created", "chart.published")

    def test_properties(self):
        chart = self.client.charts.create()

        time.sleep(2)

        event_log_item = self.client.event_log.list().current()

        assert_that(event_log_item.id > 0).is_true()
        assert_that(event_log_item.type).is_equal_to("chart.created")
        assert_that(event_log_item.timestamp).is_not_none()
        assert_that(event_log_item.data).is_equal_to({"key": chart.key, "workspaceKey": self.workspace.key})
