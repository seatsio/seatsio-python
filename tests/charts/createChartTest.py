from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assertThat


class CreateChartTest(SeatsioClientTest):

    def testDefaultParameters(self):
        chart = self.client.charts.create()

        assertThat(chart.id).isNotZero()
        assertThat(chart.key).isNotBlank()
        assertThat(chart.status).isEqualTo("NOT_USED")
        assertThat(chart.name).isEqualTo("Untitled chart")
        assertThat(chart.publishedVersionThumbnailUrl).isNotBlank()
        assertThat(chart.draftVersionThumbnailUrl).isNone()
        assertThat(chart.events).isNone()
        assertThat(chart.tags).isEmpty()
        assertThat(chart.archived).isFalse()

        drawing = self.client.charts.retrievePublishedVersion(chart.key)
        assertThat(drawing.venueType).isEqualTo("MIXED")
        assertThat(drawing.categories.list).isEmpty()

    def testName(self):
        chart = self.client.charts.create(name="aChart")

        assertThat(chart.name).isEqualTo("aChart")
        drawing = self.client.charts.retrievePublishedVersion(chart.key)
        assertThat(drawing.venueType).isEqualTo("MIXED")
        assertThat(drawing.categories.list).isEmpty()

    def testVenueType(self):
        chart = self.client.charts.create(venue_type="BOOTHS")

        assertThat(chart.name).isEqualTo("Untitled chart")
        drawing = self.client.charts.retrievePublishedVersion(chart.key)
        assertThat(drawing.venueType).isEqualTo("BOOTHS")
        assertThat(drawing.categories.list).isEmpty()

    def testCategories(self):
        chart = self.client.charts.create(
            categories=[
                {"key": 1, "label": "Category 1", "color": "#aaaaaa"},
                {"key": 2, "label": "Category 2", "color": "#bbbbbb"}
            ])

        assertThat(chart.name).isEqualTo("Untitled chart")
        drawing = self.client.charts.retrievePublishedVersion(chart.key)
        assertThat(drawing.venueType).isEqualTo("MIXED")
        assertThat(drawing.categories.list).containsExactlyInAnyOrder(
            {"key": 1, "label": "Category 1", "color": "#aaaaaa"},
            {"key": 2, "label": "Category 2", "color": "#bbbbbb"}
        )
