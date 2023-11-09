from datetime import datetime

from seatsio import TableBookingConfig, Category
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrieveEventTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        retrieved_event = self.client.events.retrieve(event.key)

        assert_that(retrieved_event.id).is_not_zero()
        assert_that(retrieved_event.key).is_not_none()
        assert_that(retrieved_event.is_event_in_season).is_false()
        assert_that(retrieved_event.chart_key).is_equal_to(chart_key)
        assert_that(retrieved_event.table_booking_config).is_equal_to(TableBookingConfig.inherit())
        assert_that(retrieved_event.supports_best_available).is_true()
        assert_that(retrieved_event.for_sale_config).is_none()
        assert_that(retrieved_event.created_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)
        assert_that(retrieved_event.updated_on).is_none()
        assert_that(retrieved_event.categories).has_size(3)
        assert_that(retrieved_event.categories).contains_exactly(
            Category(9, 'Cat1', '#87A9CD', False),
            Category(10, 'Cat2', '#5E42ED', False),
            Category('string11', 'Cat3', '#5E42BB', False)
        )
        assert_that(retrieved_event.partial_season_keys_for_event).is_none()

def test_retrieve_season(self):
        chart_key = self.create_test_chart()
        season = self.client.seasons.create(chart_key)

        retrieved_season = self.client.events.retrieve(season.key)

        assert_that(retrieved_season.id).is_not_zero()
        assert_that(retrieved_season.key).is_not_none()
        assert_that(retrieved_season.partial_season_keys).is_empty()
        assert_that(retrieved_season.events).is_empty()
        assert_that(retrieved_season.chart_key).is_equal_to(chart_key)
        assert_that(retrieved_season.table_booking_config).is_equal_to(TableBookingConfig.inherit())
        assert_that(retrieved_season.supports_best_available).is_true()
        assert_that(retrieved_season.for_sale_config).is_none()
        assert_that(retrieved_season.created_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)
        assert_that(retrieved_season.updated_on).is_none()
        assert_that(retrieved_season.categories).contains_exactly(
            Category(9, 'Cat1', '#87A9CD', False),
            Category(10, 'Cat2', '#5E42ED', False),
            Category('string11', 'Cat3', '#5E42BB', False)
        )
        assert_that(retrieved_season.partial_season_keys_for_event).is_none()
