from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CopyDraftVersionTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create("oldname")
        self.client.events.create(chart.key)
        self.client.charts.update(chart.key, "newname")

        copied_chart = self.client.charts.copy_draft_version(chart.key)

        assert_that(copied_chart.name).is_equal_to("newname (copy)")
