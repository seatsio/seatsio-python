from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrievePublishedVersionTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create("chartName")

        published_drawing = self.client.charts.retrieve_published_version(chart.key)

        assert_that(published_drawing.name).is_equal_to("chartName")
