from datetime import datetime

from seatsio import SocialDistancingRuleset, TableBookingConfig
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

    def test_social_distancing_ruleset_key_is_optional(self):
        chart_key = self.create_test_chart()
        self.client.charts.save_social_distancing_rulesets(chart_key, {
            'ruleset1': SocialDistancingRuleset(name='My first ruleset'),
        })

        event = self.client.events.create(chart_key, social_distancing_ruleset_key='ruleset1')

        assert_that(event.social_distancing_ruleset_key).is_equal_to('ruleset1')
