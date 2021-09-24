from seatsio.domain import EventObjectInfo
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrieveEventObjectInfoTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")

        assert_that(object_info.status).is_equal_to(EventObjectInfo.FREE)
        assert_that(object_info.for_sale).is_true()
