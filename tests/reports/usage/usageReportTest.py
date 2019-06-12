from seatsio.domain import Month
from tests.seatsioClientTest import SeatsioClientTest


class UsageReportTest(SeatsioClientTest):

    def setUp(self):
        super(UsageReportTest, self).setUp()

    def test_summary_for_all_months(self):
        report = self.client.usage_reports.summary_for_all_months()

    def test_details_for_month(self):
        report = self.client.usage_reports.details_for_month(Month(2019, 5))

    def test_details_for_event_in_month(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)
        report = self.client.usage_reports.details_for_event_in_month(event.id, Month(2019, 5))
