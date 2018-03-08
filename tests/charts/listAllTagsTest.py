from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListAllTagsTest(SeatsioClientTest):

    def test(self):
        chart1 = self.client.charts.create()
        self.client.charts.add_tag(chart1.key, "tag1")
        self.client.charts.add_tag(chart1.key, "tag2")

        chart2 = self.client.charts.create()
        self.client.charts.add_tag(chart2.key, "tag3")

        tags = self.client.charts.list_all_tags()

        assert_that(tags).contains_exactly_in_any_order("tag1", "tag2", "tag3")
