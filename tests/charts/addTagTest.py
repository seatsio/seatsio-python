from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assertThat


class AddTagTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts().create()

        self.client.charts().addTag(chart.key, "tag1")
        self.client.charts().addTag(chart.key, "tag2")

        retrievedChart = self.client.charts().retrieve(chart.key)
        assertThat(retrievedChart.tags).containsExactlyInAnyOrder("tag1", "tag2")

    def testSpecialCharacters(self):
        chart = self.client.charts().create()

        self.client.charts().addTag(chart.key, "'tag1:-'<>")

        retrievedChart = self.client.charts().retrieve(chart.key)
        assertThat(retrievedChart.tags).containsExactlyInAnyOrder("'tag1:-'<>")
