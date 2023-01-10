from datetime import datetime

from seatsio import TableBookingConfig
from seatsio.events.objectProperties import ObjectProperties
from seatsio.events.statusChangeRequest import StatusChangeRequest
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListStatusChangesTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.change_object_status_in_batch([
            StatusChangeRequest(event.key, ["A-1"], "status1"),
            StatusChangeRequest(event.key, ["A-1"], "status2"),
            StatusChangeRequest(event.key, ["A-1"], "status3")
        ])
        self.wait_for_status_changes(event, 3)

        status_changes = self.client.events.status_changes(event.key).list()

        assert_that(status_changes).extracting("status").contains_exactly("status3", "status2", "status1")

    def test_propertiesOfStatusChange(self):
        now = datetime.utcnow()
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        object_properties = ObjectProperties("A-1", {"foo": "bar"})
        self.client.events.change_object_status(event.key, object_properties, "status1", order_id="order1")
        self.wait_for_status_changes(event, 1)

        status_changes = self.client.events.status_changes(event.key).list()
        status_change = status_changes[0]

        assert_that(status_change.id).is_not_zero()
        assert_that(status_change.date).is_between_now_minus_and_plus_minutes(now, 1)
        assert_that(status_change.status).is_equal_to("status1")
        assert_that(status_change.object_label).is_equal_to("A-1")
        assert_that(status_change.event_id).is_equal_to(event.id)
        assert_that(status_change.extra_data).is_equal_to({"foo": "bar"})
        assert_that(status_change.origin.type).is_equal_to("API_CALL")
        assert_that(status_change.origin.ip).is_not_none()
        assert_that(status_change.is_present_on_chart).is_true()
        assert_that(status_change.not_present_on_chart_reason).is_none()

    def test_propertiesOfStatusChange_holdToken(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()
        self.client.events.hold(event.key, ["A-1"], hold_token.hold_token)
        self.wait_for_status_changes(event, 1)

        status_changes = self.client.events.status_changes(event.key).list()
        status_change = status_changes[0]

        assert_that(status_change.hold_token).is_equal_to(hold_token.hold_token)

    def test_propertiesOfStatusChange_originWithoutIp(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()
        self.client.events.hold(event.key, ["A-1"], hold_token.hold_token)
        self.client.hold_tokens.expire_in_minutes(hold_token.hold_token, 0)
        self.wait_for_status_changes(event, 2)

        status_changes = self.client.events.status_changes(event.key).list()

        assert_that(status_changes[0].origin.ip).is_none()

    def test_notPresentOnChartAnymore(self):
        chart_key = self.create_test_chart_with_tables()
        event = self.client.events.create(chart_key, table_booking_config=TableBookingConfig.all_by_table())
        self.client.events.book(event.key, ["T1"])
        self.client.events.update(event.key, table_booking_config=TableBookingConfig.all_by_seat())
        self.wait_for_status_changes(event, 1)

        status_changes = self.client.events.status_changes(event.key).list()
        status_change = status_changes[0]

        assert_that(status_change.is_present_on_chart).is_false()
        assert_that(status_change.not_present_on_chart_reason).is_equal_to("SWITCHED_TO_BOOK_BY_SEAT")

    def test_filter(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.change_object_status_in_batch([
            StatusChangeRequest(event.key, ["A-1"], "booked"),
            StatusChangeRequest(event.key, ["A-2"], "booked"),
            StatusChangeRequest(event.key, ["B-1"], "booked"),
            StatusChangeRequest(event.key, ["A-3"], "booked")
        ])
        self.wait_for_status_changes(event, 4)

        status_changes = self.client.events.status_changes(event.key, filter = "A-").list()

        assert_that(status_changes).extracting("object_label").contains_exactly("A-3", "A-2", "A-1")

    def test_sort_asc(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.change_object_status_in_batch([
            StatusChangeRequest(event.key, ["A-1"], "booked"),
            StatusChangeRequest(event.key, ["A-2"], "booked"),
            StatusChangeRequest(event.key, ["B-1"], "booked"),
            StatusChangeRequest(event.key, ["A-3"], "booked")
        ])
        self.wait_for_status_changes(event, 4)

        status_changes = self.client.events.status_changes(event.key, sort_field = "objectLabel").list()

        assert_that(status_changes).extracting("object_label").contains_exactly("A-1", "A-2", "A-3", "B-1")

    def test_sort_asc_page_before(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.change_object_status_in_batch([
            StatusChangeRequest(event.key, ["A-1"], "booked"),
            StatusChangeRequest(event.key, ["A-2"], "booked"),
            StatusChangeRequest(event.key, ["B-1"], "booked"),
            StatusChangeRequest(event.key, ["A-3"], "booked")
        ])
        self.wait_for_status_changes(event, 4)

        lister = self.client.events.status_changes(event.key, sort_field="objectLabel")
        status_changes = lister.page_before(lister.list()[2].id, 2).items

        assert_that(status_changes).extracting("object_label").contains_exactly("A-1", "A-2")

    def test_sort_asc_page_after(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.change_object_status_in_batch([
            StatusChangeRequest(event.key, ["A-1"], "booked"),
            StatusChangeRequest(event.key, ["A-2"], "booked"),
            StatusChangeRequest(event.key, ["B-1"], "booked"),
            StatusChangeRequest(event.key, ["A-3"], "booked")
        ])
        self.wait_for_status_changes(event, 4)

        lister = self.client.events.status_changes(event.key, sort_field="objectLabel")
        status_changes = lister.page_after(lister.list()[0].id, 2).items

        assert_that(status_changes).extracting("object_label").contains_exactly("A-2", "A-3")

    def test_sort_desc(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.change_object_status_in_batch([
            StatusChangeRequest(event.key, ["A-1"], "booked"),
            StatusChangeRequest(event.key, ["A-2"], "booked"),
            StatusChangeRequest(event.key, ["B-1"], "booked"),
            StatusChangeRequest(event.key, ["A-3"], "booked")
        ])
        self.wait_for_status_changes(event, 4)

        status_changes = self.client.events.status_changes(event.key, sort_field = "objectLabel", sort_direction="desc").list()

        assert_that(status_changes).extracting("object_label").contains_exactly("B-1", "A-3", "A-2", "A-1")
