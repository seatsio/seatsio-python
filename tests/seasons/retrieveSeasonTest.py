from datetime import datetime

from seatsio import TableBookingConfig
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrieveSeasonTest(SeatsioClientTest):

    def test_retrieve_season(self):
        chart_key = self.create_test_chart()
        season = self.client.seasons.create(chart_key)

        retrieved_season = self.client.seasons.retrieve(season.key)

        assert_that(retrieved_season.id).is_not_zero()
        assert_that(retrieved_season.key).is_not_none()
        assert_that(retrieved_season.partial_season_keys).is_empty()
        assert_that(retrieved_season.events).is_empty()

        season_event = retrieved_season.season_event
        assert_that(season_event.id).is_not_zero()
        assert_that(season_event.key).is_equal_to(season.key)
        assert_that(season_event.chart_key).is_equal_to(chart_key)
        assert_that(season_event.table_booking_config).is_equal_to(TableBookingConfig.inherit())
        assert_that(season_event.supports_best_available).is_true()
        assert_that(season_event.for_sale_config).is_none()
        assert_that(season_event.created_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)
        assert_that(season_event.updated_on).is_none()
