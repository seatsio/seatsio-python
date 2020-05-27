from seatsio.domain import ChartReport, ChartReportItem
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ChartReportsTest(SeatsioClientTest):

    def test_reportItemProperties(self):
        chart_key = self.create_test_chart()

        report = self.client.charts.reports.by_label(chart_key)

        assert_that(report).is_instance(ChartReport)
        report_item = report.get("A-1")[0]
        assert_that(report_item).is_instance(ChartReportItem)
        assert_that(report_item.label).is_equal_to("A-1")
        assert_that(report_item.labels).is_equal_to({"own": {"label": "1", "type": "seat"}, "parent": {"label": "A", "type": "row"}})
        assert_that(report_item.category_label).is_equal_to("Cat1")
        assert_that(report_item.category_key).is_equal_to("9")
        assert_that(report_item.object_type).is_equal_to("seat")
        assert_that(report_item.section).is_none()
        assert_that(report_item.entrance).is_none()
        assert_that(report_item.capacity).is_none()
        assert_that(report_item.left_neighbour).is_none()
        assert_that(report_item.right_neighbour).is_equal_to("A-2")

    def test_reportItemPropertiesForGA(self):
        chart_key = self.create_test_chart()

        report = self.client.charts.reports.by_label(chart_key)

        assert_that(report).is_instance(ChartReport)
        report_item = report.get("GA1")[0]
        assert_that(report_item).is_instance(ChartReportItem)
        assert_that(report_item.label).is_equal_to("GA1")
        assert_that(report_item.object_type).is_equal_to("generalAdmission")
        assert_that(report_item.category_label).is_equal_to("Cat1")
        assert_that(report_item.category_key).is_equal_to("9")
        assert_that(report_item.section).is_none()
        assert_that(report_item.entrance).is_none()
        assert_that(report_item.capacity).is_equal_to(100)

    def testByLabel(self):
        chart_key = self.create_test_chart()

        report = self.client.charts.reports.by_label(chart_key)

        assert_that(report).is_instance(ChartReport)
        assert_that(report.get("A-1")).has_size(1)
        assert_that(report.get("A-2")).has_size(1)
