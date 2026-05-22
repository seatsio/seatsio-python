from seatsio import Channel, ChannelCreationParams
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that



class AddChannelsTest(SeatsioClientTest):

    def test_addChannel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.channels.add(event.key, 'channelKey1', 'channel 1', '#FFFF98', 1, ['A-1', 'A-2'])
        self.client.events.channels.add(event.key, 'channelKey2', 'channel 2', '#FFFF99', 2, ['A-3'])

        channels = self.client.events.retrieve(event.key).channels
        assert_that(channels).is_equal_to([
            Channel(key='channelKey1', name='channel 1', color='#FFFF98', index=1, objects=['A-1', 'A-2'], area_places={}, id=channels[0].id),
            Channel(key='channelKey2', name='channel 2', color='#FFFF99', index=2, objects=['A-3'], area_places={}, id=channels[1].id)
        ])


    def test_addMultipleChannels(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.channels.add_multiple(event.key, [
            ChannelCreationParams(key="channelKey1", name="channel 1", color="#FFFF98", index=1, objects=['A-1', 'A-2']),
            ChannelCreationParams(key="channelKey2", name="channel 2", color="#FFFF99", index=2, objects=['A-3'])
        ])

        channels = self.client.events.retrieve(event.key).channels
        assert_that(channels).is_equal_to([
            Channel(key='channelKey1', name='channel 1', color='#FFFF98', index=1, objects=['A-1', 'A-2'], area_places={}, id=channels[0].id),
            Channel(key='channelKey2', name='channel 2', color='#FFFF99', index=2, objects=['A-3'], area_places={}, id=channels[1].id)
        ])


    def test_indexIsOptional(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.channels.add(event.key, 'channelKey1', 'channel 1', '#FFFF98', objects=['A-1', 'A-2'])

        channels = self.client.events.retrieve(event.key).channels

        assert_that(channels).is_equal_to([
            Channel(key='channelKey1', name='channel 1', color='#FFFF98', index=None, objects=['A-1', 'A-2'], area_places={}, id=channels[0].id),
        ])

    def test_objectsAreOptional(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.channels.add(event.key, 'channelKey1', 'channel 1', '#FFFF98', index=1)

        channels = self.client.events.retrieve(event.key).channels

        assert_that(channels).is_equal_to([
            Channel(key='channelKey1', name='channel 1', color='#FFFF98', index=1, objects=[], area_places={}, id=channels[0].id),
        ])

    def test_areaPlaces(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.channels.add(event.key, 'channelKey1', 'channel 1', '#FFFF98', 1, ['A-1', 'A-2'], area_places={'GA1': 5})

        channels = self.client.events.retrieve(event.key).channels

        assert_that(channels).is_equal_to([
            Channel(key='channelKey1', name='channel 1', color='#FFFF98', index=1, objects=['A-1', 'A-2'], area_places={'GA1': 5}, id=channels[0].id),
        ])
