from datetime import datetime

from seatsio.events.objectProperties import ObjectProperties
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListStatusChangesTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.change_object_status(event.key, ["A-1"], status="status1")
        self.client.events.change_object_status(event.key, ["A-1"], status="status2")
        self.client.events.change_object_status(event.key, ["A-1"], status="status3")

        status_changes = self.client.events.list_status_changes(event.key)

        assert_that(status_changes).extracting("status").contains_exactly("status3", "status2", "status1")

    def test_propertiesOfSTatusChange(self):
        now = datetime.utcnow()
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        object_properties = ObjectProperties("A-1", {"foo": "bar"})
        self.client.events.change_object_status(event.key, object_properties, "status1", order_id="order1")

        status_changes = self.client.events.list_status_changes(event.key)
        status_change = status_changes[0]

        assert_that(status_change.id).is_not_zero()
        assert_that(status_change.date).is_between_now_minus_and_plus_minutes(now, 1)
        assert_that(status_change.status).is_equal_to("status1")
        assert_that(status_change.object_label).is_equal_to("A-1")
        assert_that(status_change.event_id).is_equal_to(event.id)
        assert_that(status_change.extra_data).is_equal_to({"foo": "bar"})

    def test_filter(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.book(event.key, ["A-1"])
        self.client.events.book(event.key, ["A-2"])
        self.client.events.book(event.key, ["B-1"])
        self.client.events.book(event.key, ["A-3"])

        status_changes = self.client.events.list_status_changes(event.key, filter = "A-")

        assert_that(status_changes).extracting("object_label").contains_exactly("A-3", "A-2", "A-1")

    def test_sort_asc(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.book(event.key, ["A-1"])
        self.client.events.book(event.key, ["A-2"])
        self.client.events.book(event.key, ["B-1"])
        self.client.events.book(event.key, ["A-3"])

        status_changes = self.client.events.list_status_changes(event.key, sort_field = "objectLabel")

        assert_that(status_changes).extracting("object_label").contains_exactly("A-1", "A-2", "A-3", "B-1")

    def test_sort_desc(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.book(event.key, ["A-1"])
        self.client.events.book(event.key, ["A-2"])
        self.client.events.book(event.key, ["B-1"])
        self.client.events.book(event.key, ["A-3"])

        status_changes = self.client.events.list_status_changes(event.key, sort_field = "objectLabel", sort_direction="desc")

        assert_that(status_changes).extracting("object_label").contains_exactly("B-1", "A-3", "A-2", "A-1")