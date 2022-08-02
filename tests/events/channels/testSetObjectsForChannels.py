from seatsio import Channel
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class SetObjectsForChannelsTest(SeatsioClientTest):

    def test_setObjectsForChannels(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.channels.replace(event.key, {
            'channelKey1': Channel(name='channel 1', color='#00FF00', index=1),
            'channelKey2': Channel(name='channel 2', color='#FF0000', index=2),
        })

        self.client.events.channels.set_objects(event.key, {
            "channelKey1": ["A-1", "A-2"],
            "channelKey2": ["A-3"]
        })

        retrieved_channels = self.client.events.retrieve(event.key).channels
        assert_that(retrieved_channels[0].objects).is_equal_to(["A-1", "A-2"])
        assert_that(retrieved_channels[1].objects).is_equal_to(["A-3"])
