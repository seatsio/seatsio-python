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
        assert_that(retrieved_event.chartKey).is_equal_to(chart.key)
        assert_that(retrieved_event.bookWholeTables).is_false()
        assert_that(retrieved_event.forSaleConfig).is_none()
        assert_that(retrieved_event.createdOn).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)
        assert_that(retrieved_event.updatedOn).is_none()
