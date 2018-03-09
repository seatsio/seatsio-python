from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class PublishDraftVersionTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create("oldname")
        self.client.events.create(chart.key)
        self.client.charts.update(key=chart.key, new_name="newname")

        self.client.charts.publish_draft_version(chart.key)

        retrieved_chart = self.client.charts.retrieve(chart.key)
        assert_that(retrieved_chart.name).is_equal_to("newname")
        assert_that(retrieved_chart.status).is_equal_to("PUBLISHED")
