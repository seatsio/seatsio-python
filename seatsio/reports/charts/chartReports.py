from seatsio.domain import ChartReport


class ChartReports:

    def __init__(self, http_client):
        self.http_client = http_client

    def by_label(self, chart_key, book_whole_tables=None):
        return self.__fetch_report("byLabel", chart_key, book_whole_tables)

    def by_object_type(self, chart_key, book_whole_tables=None):
        return self.__fetch_report("byObjectType", chart_key, book_whole_tables)

    def summary_by_object_type(self, chart_key, book_whole_tables=None):
        return self.__fetch_summary_report("byObjectType", chart_key, book_whole_tables)

    def by_category_key(self, chart_key, book_whole_tables=None):
        return self.__fetch_report("byCategoryKey", chart_key, book_whole_tables)

    def summary_by_category_key(self, chart_key, book_whole_tables=None):
        return self.__fetch_summary_report("byCategoryKey", chart_key, book_whole_tables)

    def by_category_label(self, chart_key, book_whole_tables=None):
        return self.__fetch_report("byCategoryLabel", chart_key, book_whole_tables)

    def summary_by_category_label(self, chart_key, book_whole_tables=None):
        return self.__fetch_summary_report("byCategoryLabel", chart_key, book_whole_tables)

    def by_section(self, chart_key, book_whole_tables=None):
        return self.__fetch_report("bySection", chart_key, book_whole_tables)

    def summary_by_section(self, chart_key, book_whole_tables=None):
        return self.__fetch_summary_report("bySection", chart_key, book_whole_tables)

    def __fetch_report(self, report_type, chart_key, book_whole_tables):
        url = "/reports/charts/{key}/{reportType}"
        query_params = {"bookWholeTables": book_whole_tables} if book_whole_tables is not None else {}
        body = self.http_client.url(url, key=chart_key, reportType=report_type, query_params=query_params).get()
        return ChartReport(body)

    def __fetch_summary_report(self, report_type, chart_key, book_whole_tables):
        url = "/reports/charts/{key}/{reportType}/summary"
        query_params = {"bookWholeTables": book_whole_tables} if book_whole_tables is not None else {}
        return self.http_client.url(url, key=chart_key, reportType=report_type, query_params=query_params).get()
