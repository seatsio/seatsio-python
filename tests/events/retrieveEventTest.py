from datetime import datetime

from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrieveEventTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        retrieved_event = self.client.events.retrieve(event.key)

        assert_that(retrieved_event.id).is_not_zero()
        assert_that(retrieved_event.key).is_not_none()
        assert_that(retrieved_event.chart_key).is_equal_to(chart.key)
        assert_that(retrieved_event.book_whole_tables).is_false()
        assert_that(retrieved_event.for_sale_config).is_none()
        assert_that(retrieved_event.created_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)
        assert_that(retrieved_event.updated_on).is_none()
