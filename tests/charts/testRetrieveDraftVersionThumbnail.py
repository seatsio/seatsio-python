from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrieveDraftVersionThumbnailTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create()
        self.client.events.create(chart.key)
        self.client.charts.update(chart.key, "newname")

        thumbnail = self.client.charts.retrieve_draft_version_thumbnail(chart.key)

        assert_that(thumbnail).contains("PNG")
