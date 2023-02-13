from seatsio import Channel
from seatsio.events.channelProperties import ChannelProperties
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that



class AddChannelsTest(SeatsioClientTest):

    def test_addChannel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.channels.add(event.key, 'channelKey1', 'channel 1', '#FFFF98', 1, ['A-1', 'A-2'])
        self.client.events.channels.add(event.key, 'channelKey2', 'channel 2', '#FFFF99', 2, ['A-3'])

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.channels).is_equal_to([
            Channel(key='channelKey1', name='channel 1', color='#FFFF98', index=1, objects=['A-1', 'A-2']),
            Channel(key='channelKey2', name='channel 2', color='#FFFF99', index=2, objects=['A-3'])
        ])


    def test_addMultipleChannels(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.channels.add_multiple(event.key, [
            ChannelProperties(key="channelKey1", name="channel 1", color="#FFFF98", index=1, objects=['A-1', 'A-2']),
            ChannelProperties(key="channelKey2", name="channel 2", color="#FFFF99", index=2, objects=['A-3'])
        ])

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.channels).is_equal_to([
            Channel(key='channelKey1', name='channel 1', color='#FFFF98', index=1, objects=['A-1', 'A-2']),
            Channel(key='channelKey2', name='channel 2', color='#FFFF99', index=2, objects=['A-3'])
        ])



    def test_indexIsOptional(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.channels.add(event.key, 'channelKey1', 'channel 1', '#FFFF98', objects=['A-1', 'A-2'])

        retrieved_event = self.client.events.retrieve(event.key)

        assert_that(retrieved_event.channels).is_equal_to([
            Channel(key='channelKey1', name='channel 1', color='#FFFF98', index=None, objects=['A-1', 'A-2']),
        ])

    def test_objectsAreOptional(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.channels.add(event.key, 'channelKey1', 'channel 1', '#FFFF98', index=1)

        retrieved_event = self.client.events.retrieve(event.key)

        assert_that(retrieved_event.channels).is_equal_to([
            Channel(key='channelKey1', name='channel 1', color='#FFFF98', index=1, objects=[]),
        ])
