from seatsio import Channel
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ReplaceChannelsTest(SeatsioClientTest):

    def test_updateChannels(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        self.client.events.channels.replace(event.key, {
            'channelKey1': Channel(name='channel 1', color='#00FF00', index=1),
            'channelKey2': Channel(name='channel 2', color='#FF0000', index=2),
        })

        retrieved_event = self.client.events.retrieve(event.key)

        assert_that(retrieved_event.channels).is_equal_to([
            Channel(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=[]),
            Channel(key='channelKey2', name='channel 2', color='#FF0000', index=2, objects=[])
        ])
