from seatsio.domain import ObjectStatus
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class HoldObjectsTest(SeatsioClientTest):

    def test_withHoldToken(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()

        res = self.client.events.hold(event.key, ["A-1", "A-2"], hold_token.hold_token)

        status1 = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status1.status).is_equal_to(ObjectStatus.HELD)
        assert_that(status1.hold_token).is_equal_to(hold_token.hold_token)

        status2 = self.client.events.retrieve_object_status(event.key, "A-2")
        assert_that(status2.status).is_equal_to(ObjectStatus.HELD)
        assert_that(status2.hold_token).is_equal_to(hold_token.hold_token)

        assert_that(list(res.objects)).contains_exactly_in_any_order("A-1", "A-2")

    def test_withOrderId(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()

        self.client.events.hold(event.key, ["A-1", "A-2"], hold_token=hold_token.hold_token, order_id="order1")

        status1 = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status1.order_id).is_equal_to("order1")

        status2 = self.client.events.retrieve_object_status(event.key, "A-2")
        assert_that(status2.order_id).is_equal_to("order1")
