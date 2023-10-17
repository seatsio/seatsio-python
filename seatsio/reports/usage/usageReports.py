from seatsio.domain import UsageDetailsForMonth, UsageDetailsForEventInMonth
from seatsio.domain import UsageSummaryForAllMonths


class UsageReports:

    def __init__(self, http_client):
        self.http_client = http_client

    def summary_for_all_months(self):
        url = "/reports/usage?version=2"
        body = self.http_client.url(url).get()
        return UsageSummaryForAllMonths(body)

    def details_for_month(self, month):
        url = "/reports/usage/month/" + month.serialize()
        body = self.http_client.url(url).get()
        return UsageDetailsForMonth.from_json(body)

    def details_for_event_in_month(self, event_id, month):
        url = "/reports/usage/month/" + month.serialize() + "/event/" + str(event_id)
        body = self.http_client.url(url).get()
        return UsageDetailsForEventInMonth.from_json(body)
