from seatsio import Channel
from seatsio.events.objectProperties import ObjectProperties
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class EventReportsDeepSummaryTest(SeatsioClientTest):

    def test_deepSummaryByStatus(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.deep_summary_by_status(event.key)

        assert_that(report.get("booked").get("count")).is_equal_to(1)
        assert_that(report.get("booked").get("bySection").get("NO_SECTION").get("count")).is_equal_to(1)
        assert_that(report.get("booked").get("bySection").get("NO_SECTION").get("byAvailability").get("not_available")).is_equal_to(1)

    def test_deepSummaryByObjectType(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.deep_summary_by_object_type(event.key)

        assert_that(report.get("seat").get("count")).is_equal_to(32)
        assert_that(report.get("seat").get("bySection").get("NO_SECTION").get("count")).is_equal_to(32)
        assert_that(report.get("seat").get("bySection").get("NO_SECTION").get("byAvailability").get("available")).is_equal_to(32)

    def test_deepSummaryByCategoryKey(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.deep_summary_by_category_key(event.key)

        assert_that(report.get("9").get("count")).is_equal_to(116)
        assert_that(report.get("9").get("bySection").get("NO_SECTION").get("count")).is_equal_to(116)
        assert_that(report.get("9").get("bySection").get("NO_SECTION").get("byAvailability").get("not_available")).is_equal_to(1)

    def test_deepSummaryByCategoryLabel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.deep_summary_by_category_label(event.key)

        assert_that(report.get("Cat1").get("count")).is_equal_to(116)
        assert_that(report.get("Cat1").get("bySection").get("NO_SECTION").get("count")).is_equal_to(116)
        assert_that(report.get("Cat1").get("bySection").get("NO_SECTION").get("byAvailability").get("not_available")).is_equal_to(1)

    def test_deepSummaryBySection(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.deep_summary_by_section(event.key)

        assert_that(report.get("NO_SECTION").get("count")).is_equal_to(232)
        assert_that(report.get("NO_SECTION").get("byCategoryLabel").get("Cat1").get("count")).is_equal_to(116)
        assert_that(report.get("NO_SECTION").get("byCategoryLabel").get("Cat1").get("byAvailability").get("not_available")).is_equal_to(1)

    def test_deepSummaryByZone(self):
        chart_key = self.create_test_chart_with_zones()
        event = self.client.events.create(chart_key)

        report = self.client.events.reports.deep_summary_by_zone(event.key)

        assert_that(report.get("midtrack").get("count")).is_equal_to(6032)
        assert_that(report.get("midtrack").get("byCategoryLabel").get("Mid Track Stand").get("count")).is_equal_to(6032)

    def test_deepSummaryByAvailability(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.deep_summary_by_availability(event.key)

        assert_that(report.get("not_available").get("count")).is_equal_to(1)
        assert_that(report.get("not_available").get("byCategoryLabel").get("Cat1").get("count")).is_equal_to(1)
        assert_that(report.get("not_available").get("byCategoryLabel").get("Cat1").get("bySection").get("NO_SECTION")).is_equal_to(1)

    def test_deepSummaryByAvailabilityReason(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.deep_summary_by_availability_reason(event.key)

        assert_that(report.get("booked").get("count")).is_equal_to(1)
        assert_that(report.get("booked").get("byCategoryLabel").get("Cat1").get("count")).is_equal_to(1)
        assert_that(report.get("booked").get("byCategoryLabel").get("Cat1").get("bySection").get("NO_SECTION")).is_equal_to(1)

    def test_deepSummaryByChannel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.deep_summary_by_channel(event.key)

        assert_that(report.get("NO_CHANNEL").get("count")).is_equal_to(232)
        assert_that(report.get("NO_CHANNEL").get("byCategoryLabel").get("Cat1").get("count")).is_equal_to(116)
        assert_that(report.get("NO_CHANNEL").get("byCategoryLabel").get("Cat1").get("bySection").get("NO_SECTION")).is_equal_to(116)
