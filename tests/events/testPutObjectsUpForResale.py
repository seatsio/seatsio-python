from seatsio.domain import EventObjectInfo, Channel
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class PutObjectsUpForResaleTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        res = self.client.events.put_up_for_resale(event.key, ["A-1", "A-2"], "listing1")

        a1_status = self.client.events.retrieve_object_info(event.key, "A-1")
        a2_status = self.client.events.retrieve_object_info(event.key, "A-2")
        a3_status = self.client.events.retrieve_object_info(event.key, "A-3")

        assert_that(a1_status.status).is_equal_to(EventObjectInfo.RESALE)
        assert_that(a1_status.resale_listing_id).is_equal_to("listing1")
        assert_that(a2_status.status).is_equal_to(EventObjectInfo.RESALE)
        assert_that(a2_status.resale_listing_id).is_equal_to("listing1")
        assert_that(a3_status.status).is_equal_to(EventObjectInfo.FREE)

        assert_that(list(res.objects)).contains_exactly_in_any_order("A-1", "A-2")
