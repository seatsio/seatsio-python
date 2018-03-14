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

    def test_propertiesOfSTatusChange(self):
        now = datetime.utcnow()
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.change_object_status(event.key, ["A-1"], "status1", order_id="order1")

        status_changes = self.client.events.status_changes(event.key).all()
        status_change = status_changes[0]

        assert_that(status_change.id).is_not_zero()
        assert_that(status_change.date).is_between_now_minus_and_plus_minutes(now, 1)
        assert_that(status_change.status).is_equal_to("status1")
        assert_that(status_change.objectLabel).is_equal_to("A-1")
        assert_that(status_change.eventId).is_equal_to(event.id)
        # TODO assert_that(status_change.extraData)
