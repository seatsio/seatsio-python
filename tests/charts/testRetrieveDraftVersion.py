from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrieveDraftVersionTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create()
        self.client.events.create(chart.key)
        self.client.charts.update(chart.key, "newname")

        draft_drawing = self.client.charts.retrieve_draft_version(chart.key)

        assert_that(draft_drawing.name).is_equal_to("newname")
