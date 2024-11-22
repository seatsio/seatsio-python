from seatsio import Channel, EventObjectInfo
from seatsio.events.statusChangeRequest import StatusChangeRequest
from seatsio.exceptions import SeatsioException
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ChangeObjectStatusInBatchTest(SeatsioClientTest):

    def test(self):
        chart_key1 = self.create_test_chart()
        event1 = self.client.events.create(chart_key1)
        chart_key2 = self.create_test_chart()
        event2 = self.client.events.create(chart_key2)

        res = self.client.events.change_object_status_in_batch([
            StatusChangeRequest(event1.key, ["A-1"], "lolzor", type=StatusChangeRequest.TYPE_CHANGE_STATUS_TO),
            StatusChangeRequest(event2.key, ["A-2"], "lolzor", type=StatusChangeRequest.TYPE_CHANGE_STATUS_TO)
        ])

        assert_that(self.client.events.retrieve_object_info(event1.key, "A-1").status).is_equal_to("lolzor")
        assert_that(res[0].objects["A-1"].status).is_equal_to("lolzor")

        assert_that(self.client.events.retrieve_object_info(event2.key, "A-2").status).is_equal_to("lolzor")
        assert_that(res[1].objects["A-2"].status).is_equal_to("lolzor")

    def test_channelKeys(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key, channels=[
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1"])
        ])

        res = self.client.events.change_object_status_in_batch([
            StatusChangeRequest(event.key, ["A-1"], "lolzor", channel_keys=["channelKey1"]),
        ])

        assert_that(res[0].objects["A-1"].status).is_equal_to("lolzor")

    def test_ignoreChannels(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key, channels=[
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1"])
        ])

        res = self.client.events.change_object_status_in_batch([
            StatusChangeRequest(event.key, ["A-1"], "lolzor", ignore_channels=True),
        ])

        assert_that(res[0].objects["A-1"].status).is_equal_to("lolzor")

    def test_allowed_previous_statuses(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        try:
            self.client.events.change_object_status_in_batch([
                StatusChangeRequest(event.key, ["A-1"], "lolzor", allowed_previous_statuses=['SomeOtherStatus']),
            ])
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
            self.client.events.change_object_status_in_batch([
                StatusChangeRequest(event.key, ["A-1"], "lolzor", rejected_previous_statuses=['free']),
            ])
            self.fail("expected exception")
        except SeatsioException as e:
            assert_that(e.errors).has_size(1).is_equal_to([{
                "code": "ILLEGAL_STATUS_CHANGE",
                "message": "Cannot change from [free] to [lolzor]: free is in the list of rejected previous statuses"
            }])

    def test_release(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.book(event.key, ["A-1"])

        res = self.client.events.change_object_status_in_batch([
            StatusChangeRequest(event.key, ["A-1"], type=StatusChangeRequest.RELEASE)
        ])

        assert_that(self.client.events.retrieve_object_info(event.key, "A-1").status).is_equal_to(EventObjectInfo.FREE)
        assert_that(res[0].objects["A-1"].status).is_equal_to(EventObjectInfo.FREE)

    def test_override_season_status(self):
        chart_key = self.create_test_chart()
        season = self.client.seasons.create(chart_key, event_keys=["event1"])
        self.client.events.book(season.key, ["A-1", "A-2"])

        res = self.client.events.change_object_status_in_batch([
            StatusChangeRequest("event1", ["A-1"], type=StatusChangeRequest.OVERRIDE_SEASON_STATUS)
        ])

        assert_that(res[0].objects["A-1"].status).is_equal_to(EventObjectInfo.FREE)
        a1_status = self.client.events.retrieve_object_info("event1", "A-1").status
        assert_that(a1_status).is_equal_to(EventObjectInfo.FREE)
