from datetime import datetime, date

from seatsio import TableBookingConfig, Category, Channel, ForSaleConfig
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
        assert_that(event.table_booking_config).is_equal_to(TableBookingConfig.inherit())
        assert_that(event.supports_best_available).is_equal_to(True)
        assert_that(event.for_sale_config).is_none()
        assert_that(event.created_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)
        assert_that(event.updated_on).is_none()

    def test_event_key_can_be_passed_in(self):
        chart_key = self.create_test_chart()
        events = self.client.events.create_multiple(chart_key, [
            EventProperties(event_key="event1"), EventProperties(event_key="event2")
        ])
        assert_that(events).extracting("key").contains_exactly("event1", "event2")

    def test_table_booking_config_can_be_passed_in(self):
        chart_key = self.create_test_chart_with_tables()
        events = self.client.events.create_multiple(chart_key, [
            EventProperties(table_booking_config=TableBookingConfig.custom({"T1": "BY_TABLE", "T2": "BY_SEAT"})),
            EventProperties(table_booking_config=TableBookingConfig.custom({"T1": "BY_SEAT", "T2": "BY_TABLE"}))
        ])

        assert_that(events).extracting("table_booking_config").contains_exactly(
            TableBookingConfig.custom({"T1": "BY_TABLE", "T2": "BY_SEAT"}),
            TableBookingConfig.custom({"T1": "BY_SEAT", "T2": "BY_TABLE"})
        )

    def test_object_categories_can_be_passed_in(self):
        chart_key = self.create_test_chart()

        events = self.client.events.create_multiple(chart_key, [
            EventProperties(object_categories={'A-1': 10})
        ])

        assert_that(events).extracting("object_categories").contains_exactly(
            {'A-1': 10}
        )

    def test_categories_can_be_passed_in(self):
        chart_key = self.create_test_chart()
        event_category = Category(key='eventCategory', label='Event Level Category', color='#AAABBB')
        categories = [event_category]

        events = self.client.events.create_multiple(chart_key, [
            EventProperties(categories=categories)
        ])

        assert_that(events).has_size(1)
        event = events[0]
        assert_that(event.categories).extracting("key").contains("eventCategory")

    def test_error_on_duplicate_key(self):
        try:
            chart_key = self.create_test_chart()
            self.client.events.create_multiple(chart_key, [EventProperties(event_key="e1"), EventProperties(event_key="e1")])
            self.fail("expected exception")
        except SeatsioException as e:
            assert_that(e.errors).is_not_empty()

    def test_name_can_be_passed_in(self):
        chart_key = self.create_test_chart()
        events = self.client.events.create_multiple(chart_key, [
            EventProperties(name="My event")
        ])
        assert_that(events).extracting("name").contains_exactly("My event")

    def test_date_can_be_passed_in(self):
        chart_key = self.create_test_chart()
        events = self.client.events.create_multiple(chart_key, [
            EventProperties(date=date(2022, 1, 10))
        ])
        assert_that(events).extracting("date").contains_exactly(date(2022, 1, 10))

    def test_channel_can_be_passed_in(self):
        chart_key = self.create_test_chart()
        channels = [
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1", "A-2"]),
            Channel(key='channelKey2', name='channel 2', color='#FF0000', index=2, objects=[]),
        ]

        events = self.client.events.create_multiple(chart_key, [
            EventProperties(channels=channels)
        ])

        assert_that(events).extracting("channels").contains_exactly(channels)

    def test_for_sale_config_can_be_passed_in(self):
        chart_key = self.create_test_chart()
        for_sale_config_1 = ForSaleConfig.create_new(False, ["A-1"], {"GA1": 3}, ["Cat1"])
        for_sale_config_2 = ForSaleConfig.create_new(False, ["A-2"], {"GA1": 7}, ["Cat1"])

        events = self.client.events.create_multiple(chart_key, [
            EventProperties(for_sale_config=for_sale_config_1),
            EventProperties(for_sale_config=for_sale_config_2)
        ])

        assert_that(events).extracting("for_sale_config").contains_exactly(for_sale_config_1, for_sale_config_2)
