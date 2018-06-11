from seatsio.events.objectProperties import ObjectProperties
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ChangeObjectStatusTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        res = self.client.events.change_object_status(event.key, ["A-1", "A-2"], "status_foo")

        assert_that(self.client.events.retrieve_object_status(event.key, "A-1").status).is_equal_to("status_foo")
        assert_that(self.client.events.retrieve_object_status(event.key, "A-2").status).is_equal_to("status_foo")
        assert_that(self.client.events.retrieve_object_status(event.key, "A-3").status).is_equal_to("free")
        assert_that(res.labels).is_equal_to({
            "A-1": {"own": {"label": "1", "type": "seat"}, "parent": {"label": "A", "type": "row"}},
            "A-2": {"own": {"label": "2", "type": "seat"}, "parent": {"label": "A", "type": "row"}}
        })

    def test_hold_token(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()
        self.client.events.hold(event.key, ["A-1", "A-2"], hold_token.hold_token)

        self.client.events.change_object_status(event.key, ["A-1", "A-2"], "status_foo", hold_token.hold_token)

        status1 = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status1.status).is_equal_to("status_foo")
        assert_that(status1.hold_token).is_none()

        status1 = self.client.events.retrieve_object_status(event.key, "A-2")
        assert_that(status1.status).is_equal_to("status_foo")
        assert_that(status1.hold_token).is_none()

    def test_order_id(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.change_object_status(event.key, ["A-1", "A-2"], "status_foo", order_id="myOrder")

        assert_that(self.client.events.retrieve_object_status(event.key, "A-1").order_id).is_equal_to("myOrder")
        assert_that(self.client.events.retrieve_object_status(event.key, "A-2").order_id).is_equal_to("myOrder")

    def test_tickettype(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        props1 = ObjectProperties("A-1", ticket_type="Ticket Type 1")
        props2 = ObjectProperties("A-2", ticket_type="Ticket Type 2")

        self.client.events.change_object_status(event.key, [props1, props2], "status_foo")

        status1 = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status1.status).is_equal_to("status_foo")
        assert_that(status1.ticket_type).is_equal_to("Ticket Type 1")

        status2 = self.client.events.retrieve_object_status(event.key, "A-2")
        assert_that(status2.status).is_equal_to("status_foo")
        assert_that(status2.ticket_type).is_equal_to("Ticket Type 2")

    def test_quantity(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        props1 = ObjectProperties("GA1", quantity=5)
        props2 = ObjectProperties("GA2", quantity=10)

        self.client.events.change_object_status(event.key, [props1, props2], "status_foo")

        assert_that(self.client.events.retrieve_object_status(event.key, "GA1").quantity).is_equal_to(5)
        assert_that(self.client.events.retrieve_object_status(event.key, "GA2").quantity).is_equal_to(10)

    def test_extra_data(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        props1 = ObjectProperties("A-1", extra_data={"foo": "bar"})
        props2 = ObjectProperties("A-2", extra_data={"foo": "baz"})

        self.client.events.change_object_status(event.key, [props1, props2], "status_foo")

        assert_that(self.client.events.retrieve_object_status(event.key, "A-1").extra_data).is_equal_to({"foo": "bar"})
        assert_that(self.client.events.retrieve_object_status(event.key, "A-2").extra_data).is_equal_to({"foo": "baz"})
