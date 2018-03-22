from seatsio.domain import ObjectStatus
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class BookObjectsTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, ["A-1", "A-2"])

        a1_status = self.client.events.retrieve_object_status(event.key, "A-1").status
        a2_status = self.client.events.retrieve_object_status(event.key, "A-2").status
        a3_status = self.client.events.retrieve_object_status(event.key, "A-3").status

        assert_that(a1_status).is_equal_to(ObjectStatus.BOOKED)
        assert_that(a2_status).is_equal_to(ObjectStatus.BOOKED)
        assert_that(a3_status).is_equal_to(ObjectStatus.FREE)

    def test_withHoldToken(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()
        self.client.events.hold(event.key, ["A-1", "A-2"], hold_token.hold_token)

        self.client.events.book(event.key, ["A-1", "A-2"], hold_token.hold_token)

        status1 = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status1.status).is_equal_to(ObjectStatus.BOOKED)
        assert_that(status1.hold_token).is_none()

        status2 = self.client.events.retrieve_object_status(event.key, "A-2")
        assert_that(status2.status).is_equal_to(ObjectStatus.BOOKED)
        assert_that(status2.hold_token).is_none()

    def test_withOrderId(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, ["A-1", "A-2"], order_id="order1")

        status1 = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status1.order_id).is_equal_to("order1")

        status2 = self.client.events.retrieve_object_status(event.key, "A-2")
        assert_that(status2.order_id).is_equal_to("order1")
