from seatsio.domain import ObjectStatus, Channel
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

    def test_keepExtraData(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data = {"foo": "bar"}
        self.client.events.update_extra_data(event.key, "A-1", extra_data)
        hold_token = self.client.hold_tokens.create()

        self.client.events.hold(event.key, ["A-1"], hold_token.hold_token, keep_extra_data=True)

        status = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status.extra_data).is_equal_to(extra_data)

    def test_channelKeys(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()
        self.client.events.update_channels(event.key, {
            'channelKey1': Channel(name='channel 1', color='#00FF00', index=1)
        })
        self.client.events.assign_objects_to_channels(event.key, {
            "channelKey1": ["A-1", "A-2"]
        })

        self.client.events.hold(event.key, ["A-1"], hold_token=hold_token.hold_token, channel_keys=["channelKey1"])

        status = self.client.events.retrieve_object_status(event.key, "A-1")
        assert_that(status.status).is_equal_to(ObjectStatus.HELD)
