from seatsio.domain import Event, Zone
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListAllChartsTest(SeatsioClientTest):

    def test_all(self):
        chart1 = self.client.charts.create()
        chart2 = self.client.charts.create()
        chart3 = self.client.charts.create()

        charts = self.client.charts.list()

        assert_that(charts).extracting("key").contains_exactly(chart3.key, chart2.key, chart1.key)

    def test_filter(self):
        chart1 = self.client.charts.create(name="some stadium")
        chart2 = self.client.charts.create(name="a theatre")
        chart3 = self.client.charts.create(name="some other stadium")

        charts = self.client.charts.list(chart_filter="stadium")

        assert_that(charts).extracting("key").contains_exactly(chart3.key, chart1.key)

    def test_tag(self):
        chart1 = self.__chart_with_tag(tag="tag1")
        chart2 = self.client.charts.create()
        chart3 = self.__chart_with_tag(tag="tag1")

        charts = self.client.charts.list(tag="tag1")

        assert_that(charts).extracting("key").contains_exactly(chart3.key, chart1.key)

    def test_tag_and_filter(self):
        chart1 = self.__chart_with_tag(name="some stadium", tag="tag1")
        chart2 = self.__chart_with_tag(tag="tag1")
        chart3 = self.__chart_with_tag(name="some other stadium")
        chart4 = self.client.charts.create()

        charts = self.client.charts.list(chart_filter="stadium", tag="tag1")

        assert_that(charts).extracting("key").contains_exactly(chart1.key)

    def test_expand_all(self):
        chart = self.create_test_chart_with_zones()
        event1 = self.client.events.create(chart)
        event2 = self.client.events.create(chart)

        retrieved_charts = self.client.charts.list(expand_events=True, expand_validation=True, expand_venue_type=True, expand_zones=True)

        assert_that(retrieved_charts[0].events[0]).is_instance(Event)
        assert_that(retrieved_charts[0].events).extracting("id").contains_exactly(event2.id, event1.id)
        assert_that(retrieved_charts[0].validation).is_equal_to({"errors": [], "warnings": []})
        assert_that(retrieved_charts[0].venue_type).is_equal_to("WITH_ZONES")
        assert_that(retrieved_charts[0].zones).contains_exactly(Zone({"key": "finishline", "label": "Finish Line"}), Zone({"key": "midtrack", "label": "Mid Track"}))

    def test_expand_none(self):
            chart = self.create_test_chart_with_zones()

            retrieved_charts = self.client.charts.list()

            assert_that(retrieved_charts[0].events).is_none()
            assert_that(retrieved_charts[0].validation).is_none()
            assert_that(retrieved_charts[0].venue_type).is_none()
            assert_that(retrieved_charts[0].zones).is_none()

    def __chart_with_tag(self, name=None, tag=None):
            chart = self.client.charts.create(name)
            self.client.charts.add_tag(chart.key, tag)
            return chart
