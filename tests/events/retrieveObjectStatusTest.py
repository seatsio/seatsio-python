from datetime import datetime

from seatsio import ObjectStatus
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrieveObjectStatusTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        object_status = self.client.events.retrieve_object_status(event.key, "A-1")

        assert_that(object_status.status).is_equal_to(ObjectStatus.FREE)