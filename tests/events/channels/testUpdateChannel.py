from seatsio import Channel
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class UpdateChannelsTest(SeatsioClientTest):

    def test_updateName(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.channels.add(event.key, 'channelKey1', 'channel 1', '#FFFF98', 1, ['A-1', 'A-2'])

        self.client.events.channels.update(event.key, 'channelKey1', name='new channel name')

        channels = self.client.events.retrieve(event.key).channels
        assert_that(channels).is_equal_to([
            Channel(key='channelKey1', name='new channel name', color='#FFFF98', index=1, objects=['A-1', 'A-2'], area_places=None, id=channels[0].id)
        ])

    def test_updateColor(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.channels.add(event.key, 'channelKey1', 'channel 1', '#FFFF98', 1, ['A-1', 'A-2'])

        self.client.events.channels.update(event.key, 'channelKey1', color='red')

        channels = self.client.events.retrieve(event.key).channels
        assert_that(channels).is_equal_to([
            Channel(key='channelKey1', name='channel 1', color='red', index=1, objects=['A-1', 'A-2'], area_places=None, id=channels[0].id)
        ])

    def test_updateObjects(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.channels.add(event.key, 'channelKey1', 'channel 1', '#FFFF98', 1, ['A-1', 'A-2'])

        self.client.events.channels.update(event.key, 'channelKey1', objects=['B-1', 'B-2'])

        channels = self.client.events.retrieve(event.key).channels
        assert_that(channels).is_equal_to([
            Channel(key='channelKey1', name='channel 1', color='#FFFF98', index=1, objects=['B-1', 'B-2'], area_places=None, id=channels[0].id)
        ])

    def test_updateAreaPlaces(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.channels.add(event.key, 'channelKey1', 'channel 1', '#FFFF98', 1, ['A-1', 'A-2'])

        self.client.events.channels.update(event.key, 'channelKey1', area_places={'GA1': 3})

        channels = self.client.events.retrieve(event.key).channels
        assert_that(channels).is_equal_to([
            Channel(key='channelKey1', name='channel 1', color='#FFFF98', index=1, objects=['A-1', 'A-2'], area_places={'GA1': 3}, id=channels[0].id)
        ])
