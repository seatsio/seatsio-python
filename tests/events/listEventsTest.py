from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListEventsTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create()
        event1 = self.client.events.create(chart.key)
        event2 = self.client.events.create(chart.key)
        event3 = self.client.events.create(chart.key)

        events = self.client.events.list().all()

        assert_that(events).extracting("key").contains_exactly(event3.key, event2.key, event1.key)
