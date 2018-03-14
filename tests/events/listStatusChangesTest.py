from datetime import datetime, timedelta

from seatsio import ObjectStatus
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListStatusChangesTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.change_object_status(event.key, ["A-1"], status="status1")
        self.client.events.change_object_status(event.key, ["A-1"], status="status2")
        self.client.events.change_object_status(event.key, ["A-1"], status="status3")

        status_changes = self.client.events.status_changes(event.key).all()

        assert_that(status_changes).extracting("status").contains_exactly("status3", "status2", "status1")
