from seatsio.domain import Chart, Zone
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrieveChartTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create()
        self.client.charts.add_tag(chart.key, "tag1")
        self.client.charts.add_tag(chart.key, "tag2")

        retrieved_chart = self.client.charts.retrieve(chart.key)

        assert_that(retrieved_chart).is_instance(Chart)
        assert_that(retrieved_chart.id).is_not_zero()
        assert_that(retrieved_chart.key).is_not_blank()
        assert_that(retrieved_chart.status).is_equal_to("NOT_USED")
        assert_that(retrieved_chart.name).is_equal_to("Untitled chart")
        assert_that(retrieved_chart.published_version_thumbnail_url).is_not_blank()
        assert_that(retrieved_chart.draft_version_thumbnail_url).is_none()
        assert_that(retrieved_chart.events).is_none()
        assert_that(retrieved_chart.tags).contains_exactly_in_any_order("tag1", "tag2")
        assert_that(retrieved_chart.archived).is_false()
        assert_that(retrieved_chart.zones).is_none()

    def testZones(self):
        chart = self.create_test_chart_with_zones()

        retrieved_chart = self.client.charts.retrieve(chart)

        assert_that(retrieved_chart.zones).contains_exactly(Zone({"key": "finishline", "label": "Finish Line"}), Zone({"key": "midtrack", "label": "Mid Track"}))

    def testWithEvents(self):
        chart = self.client.charts.create()
        event1 = self.client.events.create(chart.key)
        event2 = self.client.events.create(chart.key)

        retrieved_chart = self.client.charts.retrieve_with_events(chart.key)

        assert_that(retrieved_chart.events).extracting("id").contains_exactly(event2.id, event1.id)
