from datetime import datetime

from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CreateEventTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        assert_that(event.id).is_not_zero()
        assert_that(event.key).is_not_none()
        assert_that(event.chartKey).is_equal_to(chart.key)
        assert_that(event.bookWholeTables).is_false()
        assert_that(event.forSaleConfig).is_none()
        assert_that(event.createdOn).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)
        assert_that(event.updatedOn).is_none()
