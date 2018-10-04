from seatsio.domain import ChartReport


class ChartReports:

    def __init__(self, http_client):
        self.http_client = http_client

    def by_label(self, chart_key):
        return self.__fetch_report("byLabel", chart_key)

    def __fetch_report(self, report_type, chart_key):
        url = "/reports/charts/{key}/{reportType}"
        body = self.http_client.url(url, key=chart_key, reportType=report_type).get()
        return ChartReport(body)
