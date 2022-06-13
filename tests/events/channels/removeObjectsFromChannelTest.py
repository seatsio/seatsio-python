from seatsio import Channel
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class AddObjectsToChannelTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        self.client.events.channels.add(event.key, 'channelKey1', 'channel 1', '#FFFF98', 1, ['A-1', 'A-2', 'A-3', 'A-4'])

        self.client.events.channels.remove_objects(event.key, "channelKey1", ['A-3', 'A-4'])

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.channels).is_equal_to([
            Channel(key='channelKey1', name='channel 1', color='#FFFF98', index=1, objects=['A-1', 'A-2'])
        ])
