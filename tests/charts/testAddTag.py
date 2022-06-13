from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class AddTagTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create()

        self.client.charts.add_tag(chart.key, "tag1")
        self.client.charts.add_tag(chart.key, "tag2")

        retrieved_chart = self.client.charts.retrieve(chart.key)
        assert_that(retrieved_chart.tags).contains_exactly_in_any_order("tag1", "tag2")

    def testSpecialCharacters(self):
        chart = self.client.charts.create()

        self.client.charts.add_tag(chart.key, "'tag1/:-'<>")

        retrieved_chart = self.client.charts.retrieve(chart.key)
        assert_that(retrieved_chart.tags).contains_exactly_in_any_order("'tag1/:-'<>")
