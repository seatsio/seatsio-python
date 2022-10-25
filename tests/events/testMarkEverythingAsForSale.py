from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class MarkEverythingAsForSaleTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)
        self.client.events.mark_as_not_for_sale(event.key, ["o1", "o2"], None, ["cat1", "cat2"])

        self.client.events.mark_everything_as_for_sale(event.key)

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.for_sale_config).is_none()
