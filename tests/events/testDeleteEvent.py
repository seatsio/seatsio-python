from seatsio.exceptions import SeatsioException
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class DeleteEventTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        self.client.events.delete(event.key)

        try:
            self.client.events.retrieve(event.key)
            self.fail("expected an exception")
        except SeatsioException as e:
            assert_that(e.message).contains("Event not found: " + event.key + " was not found in workspace")
