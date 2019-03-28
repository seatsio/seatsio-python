from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ChartReportTest(SeatsioClientTest):

    def setUp(self):
        super(ChartReportTest, self).setUp()
        self.chart_key = self.create_test_chart()

    def test_by_label(self):
        report = self.client.charts.reports.by_label(self.chart_key)
        assert_that(report.items).has_size(34)

    def test_by_category_key(self):
        report = self.client.charts.reports.by_category_key(self.chart_key)
        assert_that(report.items).has_size(2)
        assert_that(report.items['9']).has_size(17)
        assert_that(report.items['10']).has_size(17)

    def test_by_category_label(self):
        report = self.client.charts.reports.by_category_label(self.chart_key)
        assert_that(report.items).has_size(2)
        assert_that(report.items['Cat1']).has_size(17)
        assert_that(report.items['Cat2']).has_size(17)
