from seatsio.events.objectProperties import ObjectProperties
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class EventReportsSummaryTest(SeatsioClientTest):

    def test_summaryByStatus(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.summary_by_status(event.key)

        assert_that(report.get("booked").get("count")).is_equal_to(1)
        assert_that(report.get("booked").get("bySection").get("NO_SECTION")).is_equal_to(1)
        assert_that(report.get("booked").get("byCategoryKey").get("9")).is_equal_to(1)
        assert_that(report.get("booked").get("byCategoryLabel").get("Cat1")).is_equal_to(1)

        assert_that(report.get("free").get("count")).is_equal_to(33)
        assert_that(report.get("free").get("bySection").get("NO_SECTION")).is_equal_to(33)
        assert_that(report.get("free").get("byCategoryKey").get("9")).is_equal_to(16)
        assert_that(report.get("free").get("byCategoryKey").get("10")).is_equal_to(17)
        assert_that(report.get("free").get("byCategoryLabel").get("Cat1")).is_equal_to(16)
        assert_that(report.get("free").get("byCategoryLabel").get("Cat2")).is_equal_to(17)

    def test_summaryByCategoryKey(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.summary_by_category_key(event.key)

        assert_that(report.get("9").get("count")).is_equal_to(17)
        assert_that(report.get("9").get("bySection").get("NO_SECTION")).is_equal_to(17)
        assert_that(report.get("9").get("byStatus").get("booked")).is_equal_to(1)
        assert_that(report.get("9").get("byStatus").get("free")).is_equal_to(16)

        assert_that(report.get("10").get("count")).is_equal_to(17)
        assert_that(report.get("10").get("bySection").get("NO_SECTION")).is_equal_to(17)
        assert_that(report.get("10").get("byStatus").get("free")).is_equal_to(17)

    def test_summaryByCategoryLabel(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.summary_by_category_label(event.key)

        assert_that(report.get("Cat1").get("count")).is_equal_to(17)
        assert_that(report.get("Cat1").get("bySection").get("NO_SECTION")).is_equal_to(17)
        assert_that(report.get("Cat1").get("byStatus").get("booked")).is_equal_to(1)
        assert_that(report.get("Cat1").get("byStatus").get("free")).is_equal_to(16)

        assert_that(report.get("Cat2").get("count")).is_equal_to(17)
        assert_that(report.get("Cat2").get("bySection").get("NO_SECTION")).is_equal_to(17)
        assert_that(report.get("Cat2").get("byStatus").get("free")).is_equal_to(17)

    def test_summaryBySection(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.book(event.key, [ObjectProperties("A-1", ticket_type="tt1")], order_id="order1")

        report = self.client.events.reports.summary_by_section(event.key)

        assert_that(report.get("NO_SECTION").get("count")).is_equal_to(34)
        assert_that(report.get("NO_SECTION").get("byStatus").get("booked")).is_equal_to(1)
        assert_that(report.get("NO_SECTION").get("byStatus").get("free")).is_equal_to(33)
        assert_that(report.get("NO_SECTION").get("byCategoryKey").get("9")).is_equal_to(17)
        assert_that(report.get("NO_SECTION").get("byCategoryKey").get("10")).is_equal_to(17)
        assert_that(report.get("NO_SECTION").get("byCategoryLabel").get("Cat1")).is_equal_to(17)
        assert_that(report.get("NO_SECTION").get("byCategoryLabel").get("Cat2")).is_equal_to(17)
