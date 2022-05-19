from datetime import datetime

from seatsio import SocialDistancingRuleset, TableBookingConfig
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

    def test_social_distancing_ruleset_key_is_optional(self):
        chart_key = self.create_test_chart()
        self.client.charts.save_social_distancing_rulesets(chart_key, {
            'ruleset1': SocialDistancingRuleset(name='My first ruleset'),
        })

        season = self.client.seasons.create(chart_key, social_distancing_ruleset_key='ruleset1')

        assert_that(season.social_distancing_ruleset_key).is_equal_to('ruleset1')
