from datetime import datetime

from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CreateEventTest(SeatsioClientTest):

    def test_chart_key_is_required(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        assert_that(event.id).is_not_zero()
        assert_that(event.key).is_not_none()
        assert_that(event.chart_key).is_equal_to(chart_key)
        assert_that(event.book_whole_tables).is_false()
        assert_that(event.supports_best_available).is_true()
        assert_that(event.for_sale_config).is_none()
        assert_that(event.created_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)
        assert_that(event.updated_on).is_none()

    def test_event_key_is_optional(self):
        chart = self.client.charts.create()

        event = self.client.events.create(chart.key, event_key="eventje")

        assert_that(event.key).is_equal_to("eventje")
        assert_that(event.book_whole_tables).is_false()

    def test_book_whole_tables_is_optional(self):
        chart = self.client.charts.create()

        event = self.client.events.create(chart.key, book_whole_tables=True)

        assert_that(event.key).is_not_blank()
        assert_that(event.book_whole_tables).is_true()