from datetime import datetime, date

from seatsio import TableBookingConfig, Category, Channel, ForSaleConfig
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CreateEventTest(SeatsioClientTest):

    def test_chart_key_is_required(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        assert_that(event.id).is_not_zero()
        assert_that(event.key).is_not_none()
        assert_that(event.chart_key).is_equal_to(chart_key)
        assert_that(event.table_booking_config).is_equal_to(TableBookingConfig.inherit())
        assert_that(event.supports_best_available).is_true()
        assert_that(event.for_sale_config).is_none()
        assert_that(event.created_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)
        assert_that(event.updated_on).is_none()
        assert_that(event.categories).contains_exactly(
            Category(9, 'Cat1', '#87A9CD', False),
            Category(10, 'Cat2', '#5E42ED', False),
            Category('string11', 'Cat3', '#5E42BB', False)
        )

    def test_event_key_is_optional(self):
        chart = self.client.charts.create()

        event = self.client.events.create(chart.key, event_key="eventje")

        assert_that(event.key).is_equal_to("eventje")

    def test_table_booking_mode_custom_can_be_used(self):
        chart_key = self.create_test_chart_with_tables()
        table_booking_config = TableBookingConfig.custom({"T1": "BY_TABLE", "T2": "BY_SEAT"})

        event = self.client.events.create(chart_key, table_booking_config=table_booking_config)

        assert_that(event.key).is_not_blank()
        assert_that(event.table_booking_config).is_equal_to(table_booking_config)

    def test_table_booking_mode_inherit_can_be_used(self):
        chart_key = self.create_test_chart_with_tables()

        event = self.client.events.create(chart_key, table_booking_config=TableBookingConfig.inherit())

        assert_that(event.key).is_not_blank()
        assert_that(event.table_booking_config).is_equal_to(TableBookingConfig.inherit())

    def test_object_categories_is_optional(self):
        chart_key = self.create_test_chart()

        event = self.client.events.create(chart_key, object_categories={'A-1': 10})

        assert_that(event.object_categories).is_equal_to({'A-1': 10})

    def test_categories_is_optional(self):
        chart_key = self.create_test_chart()
        event_category = Category(key='eventCategory', label='Event Level Category', color='#AAABBB')
        categories = [event_category]

        event = self.client.events.create(chart_key, categories=categories)

        assert_that(event.categories).has_size(4) # 3 categories from sampleChart.json, 1 newly created category
        assert_that(event.categories).extracting("key").contains("eventCategory")

    def test_name_is_optional(self):
        chart = self.client.charts.create()

        event = self.client.events.create(chart.key, name="My event")

        assert_that(event.name).is_equal_to("My event")

    def test_date_is_optional(self):
        chart = self.client.charts.create()

        event = self.client.events.create(chart.key, date=date(2022, 1, 10))

        assert_that(event.date).is_equal_to(date(2022, 1, 10))

    def test_channels_are_optional(self):
        chart_key = self.create_test_chart()
        channels = [
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1", "A-2"]),
            Channel(key='channelKey2', name='channel 2', color='#FF0000', index=2, objects=[]),
        ]

        event = self.client.events.create(chart_key, channels=channels)

        assert_that(event.channels).is_equal_to(channels)

    def test_for_sale_config_is_optional(self):
        chart_key = self.create_test_chart()
        for_sale_config = ForSaleConfig.create_new(False, ["A-1", "A-2"], {"GA1": 5}, ["Cat1"])

        event = self.client.events.create(chart_key, for_sale_config=for_sale_config)

        assert_that(event.for_sale_config).is_equal_to(for_sale_config)
