from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class DiscardDraftVersionTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create("oldname")
        self.client.events.create(chart.key)
        self.client.charts.update(chart.key, "newname")

        self.client.charts.discard_draft_version(chart.key)

        retrieved_chart = self.client.charts.retrieve(chart.key)
        assert_that(retrieved_chart.name).is_equal_to("oldname")
        assert_that(retrieved_chart.status).is_equal_to("PUBLISHED")
