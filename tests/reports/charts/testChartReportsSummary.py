from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ChartReportsSummaryTest(SeatsioClientTest):

    def test_summaryByObjectType(self):
        chart_key = self.create_test_chart()

        report = self.client.charts.reports.summary_by_object_type(chart_key)

        assert_that(report.get("seat").get("count")).is_equal_to(32)
        assert_that(report.get("seat").get("bySection").get("NO_SECTION")).is_equal_to(32)
        assert_that(report.get("seat").get("byCategoryKey").get("9")).is_equal_to(16)
        assert_that(report.get("seat").get("byCategoryKey").get("10")).is_equal_to(16)
        assert_that(report.get("seat").get("byCategoryLabel").get("Cat1")).is_equal_to(16)
        assert_that(report.get("seat").get("byCategoryLabel").get("Cat2")).is_equal_to(16)

        assert_that(report.get("generalAdmission").get("count")).is_equal_to(200)
        assert_that(report.get("generalAdmission").get("bySection").get("NO_SECTION")).is_equal_to(200)
        assert_that(report.get("generalAdmission").get("byCategoryKey").get("9")).is_equal_to(100)
        assert_that(report.get("generalAdmission").get("byCategoryKey").get("10")).is_equal_to(100)
        assert_that(report.get("generalAdmission").get("byCategoryLabel").get("Cat1")).is_equal_to(100)
        assert_that(report.get("generalAdmission").get("byCategoryLabel").get("Cat2")).is_equal_to(100)

    def test_summaryByObjectType_bookWholeTablesTrue(self):
        chart_key = self.create_test_chart_with_tables()

        report = self.client.charts.reports.summary_by_object_type(chart_key, 'true')

        assert_that(report.get("seat").get("count")).is_equal_to(0)
        assert_that(report.get("table").get("count")).is_equal_to(2)

    def test_summaryByCategoryKey(self):
        chart_key = self.create_test_chart()

        report = self.client.charts.reports.summary_by_category_key(chart_key)

        assert_that(report.get("9").get("count")).is_equal_to(116)
        assert_that(report.get("9").get("bySection").get("NO_SECTION")).is_equal_to(116)

        assert_that(report.get("10").get("count")).is_equal_to(116)
        assert_that(report.get("10").get("bySection").get("NO_SECTION")).is_equal_to(116)

    def test_summaryByCategoryLabel(self):
        chart_key = self.create_test_chart()

        report = self.client.charts.reports.summary_by_category_label(chart_key)

        assert_that(report.get("Cat1").get("count")).is_equal_to(116)
        assert_that(report.get("Cat1").get("bySection").get("NO_SECTION")).is_equal_to(116)

        assert_that(report.get("Cat2").get("count")).is_equal_to(116)
        assert_that(report.get("Cat2").get("bySection").get("NO_SECTION")).is_equal_to(116)

    def test_summaryBySection(self):
        chart_key = self.create_test_chart()

        report = self.client.charts.reports.summary_by_section(chart_key)

        assert_that(report.get("NO_SECTION").get("count")).is_equal_to(232)
        assert_that(report.get("NO_SECTION").get("byCategoryKey").get("9")).is_equal_to(116)
        assert_that(report.get("NO_SECTION").get("byCategoryKey").get("10")).is_equal_to(116)
        assert_that(report.get("NO_SECTION").get("byCategoryLabel").get("Cat1")).is_equal_to(116)
        assert_that(report.get("NO_SECTION").get("byCategoryLabel").get("Cat2")).is_equal_to(116)
