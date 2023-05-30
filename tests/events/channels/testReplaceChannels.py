from seatsio import Channel
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ReplaceChannelsTest(SeatsioClientTest):

    def test_updateChannels(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.channels.replace(event.key, [
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1", "A-2"]),
            Channel(key='channelKey2', name='channel 2', color='#FF0000', index=2, objects=[]),
        ])

        retrieved_event = self.client.events.retrieve(event.key)

        assert_that(retrieved_event.channels).is_equal_to([
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1", "A-2"]),
            Channel(key='channelKey2', name='channel 2', color='#FF0000', index=2, objects=[])
        ])
