from seatsio import Month
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class UsageReportTest(SeatsioClientTest):

    def test_usage_report_for_all_months(self):
        self.assert_demo_company_secret_key_set()
        client = self.create_client(self.demo_company_secret_key(), None)

        report = client.usage_reports.summary_for_all_months()

        assert_that(report.usage_cutoff_date).is_not_none()
        assert_that(len(report.usage) > 0).is_true()
        assert_that(report.usage[0].month.year).is_equal_to(2014)
        assert_that(report.usage[0].month.month).is_equal_to(2)

    def test_usage_report_month(self):
        self.assert_demo_company_secret_key_set()
        client = self.create_client(self.demo_company_secret_key(), None)

        report = client.usage_reports.details_for_month(Month(2021, 11))

        assert_that(len(report) > 0).is_true()
        assert_that(len(report[0].usage_by_chart) > 0).is_true()
        assert_that(report[0].usage_by_chart[0].usage_by_event[0].num_used_objects).is_equal_to(143)


    def test_usage_report_event_in_month(self):
            self.assert_demo_company_secret_key_set()
            client = self.create_client(self.demo_company_secret_key(), None)

            report = client.usage_reports.details_for_event_in_month(580293, Month(2021, 11))

            assert_that(len(report) > 0).is_true()
            assert_that(report[0].num_first_selections).is_equal_to(1)
