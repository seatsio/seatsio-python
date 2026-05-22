from tests.seatsioClientTest import SeatsioClientTest


class ChannelIdTest(SeatsioClientTest):

    def test_channelHasId(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.channels.add(event.key, 'channelKey1', 'channel 1', '#FFFF98', 1)

        retrieved_event = self.client.events.retrieve(event.key)
        channel = retrieved_event.channels[0]
        self.assertIsNotNone(channel.id)

    def test_areaPartitionLabel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.channels.add(event.key, 'channelKey1', 'channel 1', '#FFFF98', 1)

        retrieved_event = self.client.events.retrieve(event.key)
        channel = retrieved_event.channels[0]
        self.assertEqual(f"myArea##{channel.id}", channel.area_partition_label("myArea"))

