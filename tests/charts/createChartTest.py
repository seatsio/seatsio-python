from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assertThat


class CreateChartTest(SeatsioClientTest):

    def testDefaultParameters(self):
        chart = self.client.charts().create()

        assertThat(chart.id).isNotZero()
        assertThat(chart.key).isNotBlank()
        assertThat(chart.status).isEqualTo("NOT_USED")
        assertThat(chart.name).isEqualTo("Untitled chart")
        assertThat(chart.publishedVersionThumbnailUrl).isNotBlank()
        assertThat(chart.draftVersionThumbnailUrl).isNone()
        assertThat(chart.events).isNone()
        assertThat(chart.tags).isEmpty()
        assertThat(chart.archived).isFalse()

        drawing = self.client.charts().retrievePublishedVersion(chart.key)
        assertThat(drawing.venueType).isEqualTo("MIXED")
        assertThat(drawing.categories.list).isEmpty()

    def testName(self):
        chart = self.client.charts().create(name="aChart")

        assertThat(chart.name).isEqualTo("aChart")
        drawing = self.client.charts().retrievePublishedVersion(chart.key)
        assertThat(drawing.venueType).isEqualTo("MIXED")
        assertThat(drawing.categories.list).isEmpty()


    def testVenueType(self):
        chart = self.client.charts().create(venue_type="BOOTHS")

        assertThat(chart.name).isEqualTo("Untitled chart")
        drawing = self.client.charts().retrievePublishedVersion(chart.key)
        assertThat(drawing.venueType).isEqualTo("BOOTHS")
        assertThat(drawing.categories.list).isEmpty()
