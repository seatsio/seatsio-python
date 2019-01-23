from datetime import datetime

from seatsio.events.eventProperties import EventProperties
from seatsio.exceptions import SeatsioException
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CreateEventsTest(SeatsioClientTest):

    def test_can_create_multiple_events(self):
        chart_key = self.create_test_chart()
        events_properties = [EventProperties(), EventProperties()]
        events = self.client.events.create_multiple(chart_key, events_properties)
        assert_that(events).has_size(2).extracting("key").is_not_none()

    def test_single_event(self):
        chart_key = self.create_test_chart()
        events = self.client.events.create_multiple(chart_key, [EventProperties()])
        assert_that(events).has_size(1)
        event = events[0]
        assert_that(event.id).is_not_zero()
        assert_that(event.key).is_not_none()
        assert_that(event.chart_key).is_equal_to(chart_key)
        assert_that(event.book_whole_tables).is_false()
        assert_that(event.supports_best_available).is_none()
        assert_that(event.for_sale_config).is_none()
        assert_that(event.created_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)
        assert_that(event.updated_on).is_none()

    def test_event_key_can_be_passed_in(self):
        chart_key = self.create_test_chart()
        events = self.client.events.create_multiple(chart_key, [
            EventProperties(event_key="event1"), EventProperties(event_key="event2")
        ])
        assert_that(events).extracting("key").contains_exactly_in_any_order("event1", "event2")

    def test_book_whole_tables_can_be_passed_in(self):
        chart_key = self.create_test_chart()
        events = self.client.events.create_multiple(chart_key, [
            EventProperties(book_whole_tables=True), EventProperties(book_whole_tables=False)
        ])
        assert_that(events).extracting("book_whole_tables").contains_exactly(True, False)

    def test_table_booking_modes_can_be_passed_in(self):
        chart_key = self.create_test_chart_with_tables()
        events = self.client.events.create_multiple(chart_key, [
            EventProperties(table_booking_modes={"T1": "BY_TABLE", "T2": "BY_SEAT"}),
            EventProperties(table_booking_modes={"T1": "BY_SEAT", "T2": "BY_TABLE"})
        ])

        assert_that(events).extracting("book_whole_tables").contains_exactly(False, False)
        assert_that(events).extracting("table_booking_modes").contains_exactly(
            {"T1": "BY_TABLE", "T2": "BY_SEAT"},
            {"T1": "BY_SEAT", "T2": "BY_TABLE"}
        )

    def test_error_on_duplicate_key(self):
        try:
            chart_key = self.create_test_chart()
            self.client.events.create_multiple(chart_key, [EventProperties(event_key="e1"), EventProperties(event_key="e1")])
            self.fail("expected exception")
        except SeatsioException as e:
            assert_that(e.errors).is_not_empty()
