from seatsio.domain import EventObjectInfo, Channel
from seatsio.events.objectProperties import ObjectProperties
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ReleaseObjectsTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.book(event.key, ["A-1", "A-2"])

        res = self.client.events.release(event.key, ["A-1", "A-2"])

        a1_status = self.client.events.retrieve_object_info(event.key, "A-1").status
        a2_status = self.client.events.retrieve_object_info(event.key, "A-2").status
        a3_status = self.client.events.retrieve_object_info(event.key, "A-3").status

        assert_that(a1_status).is_equal_to(EventObjectInfo.FREE)
        assert_that(a2_status).is_equal_to(EventObjectInfo.FREE)
        assert_that(a3_status).is_equal_to(EventObjectInfo.FREE)

        assert_that(list(res.objects)).contains_exactly_in_any_order("A-1", "A-2")

    def test_withHoldToken(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()
        self.client.events.hold(event.key, ["A-1"], hold_token.hold_token)

        self.client.events.release(event.key, ["A-1"], hold_token.hold_token)

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.status).is_equal_to(EventObjectInfo.FREE)
        assert_that(object_info.hold_token).is_none()

    def test_withOrderId(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.book(event.key, ["A-1"])

        self.client.events.release(event.key, ["A-1"], order_id="order1")

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.order_id).is_equal_to("order1")

    def test_keepExtraData(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data = {"foo": "bar"}
        self.client.events.book(event.key, [ObjectProperties("A-1", extra_data=extra_data)])

        self.client.events.release(event.key, ["A-1"], keep_extra_data=True)

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.extra_data).is_equal_to(extra_data)

    def test_channelKeys(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key, channels=[
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1", "A-2"])
        ])
        self.client.events.book(event.key, ["A-1"], channel_keys=["channelKey1"])

        self.client.events.release(event.key, ["A-1"], channel_keys=["channelKey1"])

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.status).is_equal_to(EventObjectInfo.FREE)

    def test_ignoreChannels(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key, channels=[
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1", "A-2"])
        ])
        self.client.events.book(event.key, ["A-1"], channel_keys=["channelKey1"])

        self.client.events.release(event.key, ["A-1"], ignore_channels=True)

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.status).is_equal_to(EventObjectInfo.FREE)
