from seatsio.domain import EventObjectInfo, Channel
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class HoldObjectsTest(SeatsioClientTest):

    def test_withHoldToken(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()

        res = self.client.events.hold(event.key, ["A-1", "A-2"], hold_token.hold_token)

        status1 = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(status1.status).is_equal_to(EventObjectInfo.HELD)
        assert_that(status1.hold_token).is_equal_to(hold_token.hold_token)

        status2 = self.client.events.retrieve_object_info(event.key, "A-2")
        assert_that(status2.status).is_equal_to(EventObjectInfo.HELD)
        assert_that(status2.hold_token).is_equal_to(hold_token.hold_token)

        assert_that(list(res.objects)).contains_exactly_in_any_order("A-1", "A-2")

    def test_withOrderId(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()

        self.client.events.hold(event.key, ["A-1", "A-2"], hold_token.hold_token, order_id="order1")

        status1 = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(status1.order_id).is_equal_to("order1")

        status2 = self.client.events.retrieve_object_info(event.key, "A-2")
        assert_that(status2.order_id).is_equal_to("order1")

    def test_keepExtraData(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data = {"foo": "bar"}
        self.client.events.update_extra_data(event.key, "A-1", extra_data)
        hold_token = self.client.hold_tokens.create()

        self.client.events.hold(event.key, ["A-1"], hold_token.hold_token, keep_extra_data=True)

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.extra_data).is_equal_to(extra_data)

    def test_channelKeys(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key, channels=[
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1", "A-2"])
        ])
        hold_token = self.client.hold_tokens.create()

        self.client.events.hold(event.key, ["A-1"], hold_token.hold_token, channel_keys=["channelKey1"])

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.status).is_equal_to(EventObjectInfo.HELD)

    def test_ignoreChannels(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key, channels=[
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1", "A-2"])
        ])
        hold_token = self.client.hold_tokens.create()

        self.client.events.hold(event.key, ["A-1"], hold_token.hold_token, ignore_channels=True)

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.status).is_equal_to(EventObjectInfo.HELD)
