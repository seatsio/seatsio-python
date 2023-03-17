from seatsio.domain import UsageDetailsForMonth
from seatsio.domain import UsageSummaryForAllMonths, UsageDetailsForEventInMonthV1, \
    UsageDetailsForEventInMonthV2


class UsageReports:

    def __init__(self, http_client):
        self.http_client = http_client

    def summary_for_all_months(self):
        url = "/reports/usage"
        body = self.http_client.url(url).get()
        return UsageSummaryForAllMonths(body)

    def details_for_month(self, month):
        url = "/reports/usage/month/" + month.serialize()
        body = self.http_client.url(url).get()
        return UsageDetailsForMonth(body)

    def details_for_event_in_month(self, event_id, month):
        url = "/reports/usage/month/" + month.serialize() + "/event/" + str(event_id)
        body = self.http_client.url(url).get()
        if len(body) == 0 or "usageByReason" not in body[0]:
            return UsageDetailsForEventInMonthV1(body)
        else:
            return UsageDetailsForEventInMonthV2(body)
