from seatsio import Channel
from seatsio.events.objectProperties import ObjectProperties
from seatsio.exceptions import SeatsioException
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ChangeObjectStatusTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        res = self.client.events.change_object_status(event.key, ["A-1", "A-2"], "status_foo")

        assert_that(self.client.events.retrieve_object_info(event.key, "A-1").status).is_equal_to("status_foo")
        assert_that(self.client.events.retrieve_object_info(event.key, "A-2").status).is_equal_to("status_foo")
        assert_that(self.client.events.retrieve_object_info(event.key, "A-3").status).is_equal_to("free")

        assert_that(list(res.objects)).contains_exactly_in_any_order("A-1", "A-2")
        object = res.objects["A-1"]
        assert_that(object.status).is_equal_to("status_foo")
        assert_that(object.label).is_equal_to("A-1")
        assert_that(object.labels).is_equal_to({"own": {"label": "1", "type": "seat"}, "parent": {"label": "A", "type": "row"}})
        assert_that(object.ids).is_equal_to({"own": "1", "parent": "A"})
        assert_that(object.category_label).is_equal_to("Cat1")
        assert_that(object.category_key).is_equal_to("9")
        assert_that(object.ticket_type).is_none()
        assert_that(object.order_id).is_none()
        assert_that(object.object_type).is_equal_to("seat")
        assert_that(object.for_sale).is_true()
        assert_that(object.section).is_none()
        assert_that(object.entrance).is_none()
        assert_that(object.num_booked).is_none()
        assert_that(object.capacity).is_none()
        assert_that(object.left_neighbour).is_none()
        assert_that(object.right_neighbour).is_equal_to("A-2")

    def test_hold_token(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()
        self.client.events.hold(event.key, ["A-1", "A-2"], hold_token.hold_token)

        self.client.events.change_object_status(event.key, ["A-1", "A-2"], "status_foo", hold_token.hold_token)

        status1 = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(status1.status).is_equal_to("status_foo")
        assert_that(status1.hold_token).is_none()

        status1 = self.client.events.retrieve_object_info(event.key, "A-2")
        assert_that(status1.status).is_equal_to("status_foo")
        assert_that(status1.hold_token).is_none()

    def test_order_id(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.change_object_status(event.key, ["A-1", "A-2"], "status_foo", order_id="myOrder")

        assert_that(self.client.events.retrieve_object_info(event.key, "A-1").order_id).is_equal_to("myOrder")
        assert_that(self.client.events.retrieve_object_info(event.key, "A-2").order_id).is_equal_to("myOrder")

    def test_tickettype(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        props1 = ObjectProperties("A-1", ticket_type="Ticket Type 1")
        props2 = ObjectProperties("A-2", ticket_type="Ticket Type 2")

        self.client.events.change_object_status(event.key, [props1, props2], "status_foo")

        status1 = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(status1.status).is_equal_to("status_foo")
        assert_that(status1.ticket_type).is_equal_to("Ticket Type 1")

        status2 = self.client.events.retrieve_object_info(event.key, "A-2")
        assert_that(status2.status).is_equal_to("status_foo")
        assert_that(status2.ticket_type).is_equal_to("Ticket Type 2")

    def test_quantity(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        props1 = ObjectProperties("GA1", quantity=5)
        props2 = ObjectProperties("GA2", quantity=10)

        self.client.events.change_object_status(event.key, [props1, props2], "status_foo")

        assert_that(self.client.events.retrieve_object_info(event.key, "GA1").num_booked).is_equal_to(5)
        assert_that(self.client.events.retrieve_object_info(event.key, "GA2").num_booked).is_equal_to(10)

    def test_extra_data(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        props1 = ObjectProperties("A-1", extra_data={"foo": "bar"})
        props2 = ObjectProperties("A-2", extra_data={"foo": "baz"})

        self.client.events.change_object_status(event.key, [props1, props2], "status_foo")

        assert_that(self.client.events.retrieve_object_info(event.key, "A-1").extra_data).is_equal_to({"foo": "bar"})
        assert_that(self.client.events.retrieve_object_info(event.key, "A-2").extra_data).is_equal_to({"foo": "baz"})

    def test_keepExtraDataTrue(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data = {"foo": "bar"}
        self.client.events.update_extra_data(event.key, "A-1", extra_data)

        self.client.events.change_object_status(event.key, ["A-1"], "someStatus", keep_extra_data=True)

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.extra_data).is_equal_to(extra_data)

    def test_keepExtraDataFalse(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data = {"foo": "bar"}
        self.client.events.update_extra_data(event.key, "A-1", extra_data)

        self.client.events.change_object_status(event.key, ["A-1"], "someStatus", keep_extra_data=False)

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.extra_data).is_none()

    def test_noKeepExtraData(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data = {"foo": "bar"}
        self.client.events.update_extra_data(event.key, "A-1", extra_data)

        self.client.events.change_object_status(event.key, ["A-1"], "someStatus")

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.extra_data).is_none()

    def test_channelKeys(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key, channels=[
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1", "A-2"])
        ])

        self.client.events.change_object_status(event.key, ["A-1"], "someStatus", channel_keys=["channelKey1"])

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.status).is_equal_to("someStatus")

    def test_ignoreChannels(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key, channels=[
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1", "A-2"])
        ])

        self.client.events.change_object_status(event.key, ["A-1"], "someStatus", ignore_channels=True)

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.status).is_equal_to("someStatus")

    def test_allowed_previous_statuses(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        try:
            self.client.events.change_object_status(event.key, ["A-1"], "lolzor", allowed_previous_statuses=['SomeOtherStatus'])
            self.fail("expected exception")
        except SeatsioException as e:
            assert_that(e.errors).has_size(1).is_equal_to([{
                "code": "ILLEGAL_STATUS_CHANGE",
                "message": "Cannot change from [free] to [lolzor]: free is not in the list of allowed previous statuses"
            }])

    def test_reject_previous_statuses(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        try:
            self.client.events.change_object_status(event.key, ["A-1"], "lolzor", rejected_previous_statuses=['free'])
            self.fail("expected exception")
        except SeatsioException as e:
            assert_that(e.errors).has_size(1).is_equal_to([{
                "code": "ILLEGAL_STATUS_CHANGE",
                "message": "Cannot change from [free] to [lolzor]: free is in the list of rejected previous statuses"
            }])
