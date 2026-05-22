from seatsio import Channel, ChannelCreationParams
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ReplaceChannelsTest(SeatsioClientTest):

    def test_replaceChannels(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.channels.replace(event.key, [
            ChannelCreationParams(key='channelKey1', name='channel 1', color='#00FF00', index=1, objects=["A-1", "A-2"], area_places={"GA1": 3}),
            ChannelCreationParams(key='channelKey2', name='channel 2', color='#FF0000', index=2, objects=[]),
        ])

        channels = self.client.events.retrieve(event.key).channels

        assert_that(channels).is_equal_to([
            Channel(name='channel 1', color='#00FF00', index=1, key='channelKey1', objects=["A-1", "A-2"], area_places={"GA1": 3}, id=channels[0].id),
            Channel(name='channel 2', color='#FF0000', index=2, key='channelKey2', objects=[], area_places={}, id=channels[1].id)
        ])
