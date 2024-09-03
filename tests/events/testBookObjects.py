from seatsio.domain import EventObjectInfo, Channel
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class BookObjectsTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        res = self.client.events.book(event.key, ["A-1", "A-2"])

        a1_status = self.client.events.retrieve_object_info(event.key, "A-1").status
        a2_status = self.client.events.retrieve_object_info(event.key, "A-2").status
        a3_status = self.client.events.retrieve_object_info(event.key, "A-3").status

        assert_that(a1_status).is_equal_to(EventObjectInfo.BOOKED)
        assert_that(a2_status).is_equal_to(EventObjectInfo.BOOKED)
        assert_that(a3_status).is_equal_to(EventObjectInfo.FREE)

        assert_that(list(res.objects)).contains_exactly_in_any_order("A-1", "A-2")

    def test_sections(self):
        chart_key = self.create_test_chart_with_sections()
        event = self.client.events.create(chart_key)

        res = self.client.events.book(event.key, ["Section A-A-1", "Section A-A-2"])

        a1_status = self.client.events.retrieve_object_info(event.key, "Section A-A-1").status
        a2_status = self.client.events.retrieve_object_info(event.key, "Section A-A-2").status
        a3_status = self.client.events.retrieve_object_info(event.key, "Section A-A-3").status

        assert_that(a1_status).is_equal_to(EventObjectInfo.BOOKED)
        assert_that(a2_status).is_equal_to(EventObjectInfo.BOOKED)
        assert_that(a3_status).is_equal_to(EventObjectInfo.FREE)

        assert_that(list(res.objects)).contains_exactly_in_any_order("Section A-A-1", "Section A-A-2")
        assert_that(res.objects["Section A-A-1"].entrance).is_equal_to("Entrance 1")
        assert_that(res.objects["Section A-A-1"].section).is_equal_to("Section A")
        assert_that(res.objects["Section A-A-1"].floor).is_none()
        assert_that(res.objects["Section A-A-1"].labels).is_equal_to(
            {"own": {"label": "1", "type": "seat"}, "parent": {"label": "A", "type": "row"}, "section": "Section A",
             "entrance": {"label": "Entrance 1"}}
        )
        assert_that(res.objects["Section A-A-1"].ids).is_equal_to({"own": "1", "parent": "A", "section": "Section A"})

    def test_floors(self):
        chart_key = self.create_test_chart_with_floors()
        event = self.client.events.create(chart_key)

        res = self.client.events.book(event.key, ["S1-A-1"])

        assert_that(res.objects["S1-A-1"].floor).is_equal_to(
            {"name": "1", "displayName": "Floor 1"}
        )

    def test_withHoldToken(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()
        self.client.events.hold(event.key, ["A-1", "A-2"], hold_token.hold_token)

        self.client.events.book(event.key, ["A-1", "A-2"], hold_token.hold_token)

        status1 = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(status1.status).is_equal_to(EventObjectInfo.BOOKED)
        assert_that(status1.hold_token).is_none()

        status2 = self.client.events.retrieve_object_info(event.key, "A-2")
        assert_that(status2.status).is_equal_to(EventObjectInfo.BOOKED)
        assert_that(status2.hold_token).is_none()

    def test_withOrderId(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, ["A-1", "A-2"], order_id="order1")

        status1 = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(status1.order_id).is_equal_to("order1")

        status2 = self.client.events.retrieve_object_info(event.key, "A-2")
        assert_that(status2.order_id).is_equal_to("order1")

    def test_keepExtraData(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data = {"foo": "bar"}
        self.client.events.update_extra_data(event.key, "A-1", extra_data)

        self.client.events.book(event.key, ["A-1"], keep_extra_data=True)

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.extra_data).is_equal_to(extra_data)

    def test_channelKeys(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key, channels=[
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1", "A-2"])
        ])

        self.client.events.book(event.key, ["A-1"], channel_keys=["channelKey1"])

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.status).is_equal_to(EventObjectInfo.BOOKED)

    def test_ignoreChannels(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key, channels=[
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1", "A-2"])
        ])

        self.client.events.book(event.key, ["A-1"], ignore_channels=True)

        object_info = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_info.status).is_equal_to(EventObjectInfo.BOOKED)
