from seatsio.domain import EventObjectInfo
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class EventReportsFlatListTest(SeatsioClientTest):

    def test_flat_list_with_season_bookings_not_propagated(self):
        chart_key = self.create_test_chart()
        season = self.client.seasons.create(chart_key, number_of_events=1)
        event = season.events[0]
        self.client.events.book(season.key, ["A-1", "A-2"])
        self.client.events.book(event.key, ["A-3"])

        report_with_propagation = self.client.events.reports.flat_list(season.key)
        report_without_propagation = self.client.events.reports.with_season_bookings_not_propagated().flat_list(season.key)

        assert_that(next(item for item in report_with_propagation if item.label == "A-3").status).is_equal_to(EventObjectInfo.BOOKED)
        assert_that(next(item for item in report_without_propagation if item.label == "A-3").status).is_not_equal_to(EventObjectInfo.BOOKED)

    def test_flat_list(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.flat_list(event.key)

        assert_that(report).is_instance(list)
        assert_that(report[0]).is_instance(EventObjectInfo)
        labels = [item.label for item in report]
        assert_that(labels).is_equal_to(sorted(labels))

    def test_flat_list_properties(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.flat_list(event.key)

        first = next(item for item in report if item.label == "A-1")
        assert_that(first.status).is_equal_to("free")
        assert_that(first.label).is_equal_to("A-1")
        assert_that(first.object_type).is_equal_to("seat")

    def test_flat_list_csv(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        csv = self.client.events.reports.flat_list_csv(event.key)

        assert_that(csv).is_instance(str)
        assert_that(csv).contains("A-1")

