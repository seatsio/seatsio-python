from seatsio import Channel
from seatsio.events.statusChangeRequest import StatusChangeRequest
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ChangeObjectStatusInBatchTest(SeatsioClientTest):

    def test(self):
        chart_key1 = self.create_test_chart()
        event1 = self.client.events.create(chart_key1)
        chart_key2 = self.create_test_chart()
        event2 = self.client.events.create(chart_key2)

        res = self.client.events.change_object_status_in_batch([
            StatusChangeRequest(event1.key, ["A-1"], "lolzor"),
            StatusChangeRequest(event2.key, ["A-2"], "lolzor")
        ])

        assert_that(self.client.events.retrieve_object_info(event1.key, "A-1").status).is_equal_to("lolzor")
        assert_that(res[0].objects["A-1"].status).is_equal_to("lolzor")

        assert_that(self.client.events.retrieve_object_info(event2.key, "A-2").status).is_equal_to("lolzor")
        assert_that(res[1].objects["A-2"].status).is_equal_to("lolzor")

    def test_channelKeys(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.update_channels(event.key, {
            'channelKey1': Channel(name='channel 1', color='#00FF00', index=1)
        })
        self.client.events.assign_objects_to_channels(event.key, {
            "channelKey1": ["A-1"]
        })

        res = self.client.events.change_object_status_in_batch([
            StatusChangeRequest(event.key, ["A-1"], "lolzor", channel_keys=["channelKey1"]),
        ])

        assert_that(res[0].objects["A-1"].status).is_equal_to("lolzor")

    def test_ignoreChannels(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.update_channels(event.key, {
            'channelKey1': Channel(name='channel 1', color='#00FF00', index=1)
        })
        self.client.events.assign_objects_to_channels(event.key, {
            "channelKey1": ["A-1"]
        })

        res = self.client.events.change_object_status_in_batch([
            StatusChangeRequest(event.key, ["A-1"], "lolzor", ignore_channels=True),
        ])

        assert_that(res[0].objects["A-1"].status).is_equal_to("lolzor")
