from datetime import datetime

from seatsio import TableBookingConfig, Channel, ForSaleConfig
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CreateSeasonTest(SeatsioClientTest):

    def test_chart_key_is_required(self):
        chart_key = self.create_test_chart()

        season = self.client.seasons.create(chart_key)

        assert_that(season.id).is_not_zero()
        assert_that(season.key).is_not_none()
        assert_that(season.is_top_level_season).is_true()
        assert_that(season.top_level_season_key).is_none()
        assert_that(season.partial_season_keys).is_empty()
        assert_that(season.events).is_empty()
        assert_that(season.chart_key).is_equal_to(chart_key)
        assert_that(season.table_booking_config).is_equal_to(TableBookingConfig.inherit())
        assert_that(season.supports_best_available).is_true()
        assert_that(season.for_sale_config).is_none()
        assert_that(season.created_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)
        assert_that(season.updated_on).is_none()

    def test_key_is_optional(self):
        chart = self.client.charts.create()

        season = self.client.seasons.create(chart.key, key="aSeason")

        assert_that(season.key).is_equal_to("aSeason")

    def test_number_of_events_is_optional(self):
        chart = self.client.charts.create()

        season = self.client.seasons.create(chart.key, number_of_events=2)

        assert_that(season.events).has_size(2)

    def test_event_keys_is_optional(self):
        chart = self.client.charts.create()

        season = self.client.seasons.create(chart.key, event_keys=["event1", "event2"])

        assert_that(season.events)\
            .extracting("key")\
            .contains_exactly("event1", "event2")

    def test_table_booking_mode_is_optional(self):
        chart_key = self.create_test_chart_with_tables()
        table_booking_config = TableBookingConfig.custom({"T1": "BY_TABLE", "T2": "BY_SEAT"})

        season = self.client.seasons.create(chart_key, table_booking_config=table_booking_config)

        assert_that(season.table_booking_config).is_equal_to(table_booking_config)

    def test_channels_are_optional(self):
        chart_key = self.create_test_chart()
        channels = [
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1", "A-2"]),
            Channel(key='channelKey2', name='channel 2', color='#FF0000', index=2, objects=[]),
        ]

        season = self.client.seasons.create(chart_key, channels=channels)

        assert_that(season.channels).is_equal_to(channels)

    def test_for_sale_config_optional(self):
        chart_key = self.create_test_chart()
        for_sale_config = ForSaleConfig.create_new(False, ["A-1", "A-2"], {"GA1": 5}, ["Cat1"])

        season = self.client.seasons.create(chart_key, for_sale_config=for_sale_config)

        assert_that(season.for_sale_config).is_equal_to(for_sale_config)
