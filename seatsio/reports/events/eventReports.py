from seatsio.domain import EventObjectInfo, EventReport


class EventReports:
    def __init__(self, http_client):
        self.http_client = http_client

    def by_status(self, event_key, status=None):
        return self.__fetch_report("byStatus", event_key, status)

    def summary_by_status(self, event_key):
        return self.__fetch_summary_report("byStatus", event_key)

    def deep_summary_by_status(self, event_key):
        return self.__fetch_deep_summary_report("byStatus", event_key)

    def by_object_type(self, event_key, object_type=None):
        return self.__fetch_report("byObjectType", event_key, object_type)

    def summary_by_object_type(self, event_key):
        return self.__fetch_summary_report("byObjectType", event_key)

    def deep_summary_by_object_type(self, event_key):
        return self.__fetch_deep_summary_report("byObjectType", event_key)

    def by_category_label(self, event_key, category_label=None):
        return self.__fetch_report("byCategoryLabel", event_key, category_label)

    def summary_by_category_label(self, event_key):
        return self.__fetch_summary_report("byCategoryLabel", event_key)

    def deep_summary_by_category_label(self, event_key):
        return self.__fetch_deep_summary_report("byCategoryLabel", event_key)

    def by_category_key(self, event_key, category_key=None):
        return self.__fetch_report("byCategoryKey", event_key, category_key)

    def summary_by_category_key(self, event_key):
        return self.__fetch_summary_report("byCategoryKey", event_key)

    def deep_summary_by_category_key(self, event_key):
        return self.__fetch_deep_summary_report("byCategoryKey", event_key)

    def by_label(self, event_key, label=None):
        return self.__fetch_report("byLabel", event_key, label)

    def by_order_id(self, event_key, order_id=None):
        return self.__fetch_report("byOrderId", event_key, order_id)

    def by_section(self, event_key, section=None):
        return self.__fetch_report("bySection", event_key, section)

    def summary_by_section(self, event_key):
        return self.__fetch_summary_report("bySection", event_key)

    def deep_summary_by_section(self, event_key):
        return self.__fetch_deep_summary_report("bySection", event_key)

    def by_availability(self, event_key, availability=None):
        return self.__fetch_report("byAvailability", event_key, availability)

    def summary_by_availability(self, event_key):
        return self.__fetch_summary_report("byAvailability", event_key)

    def deep_summary_by_availability(self, event_key):
        return self.__fetch_deep_summary_report("byAvailability", event_key)

    def by_availability_reason(self, event_key, availability_reason=None):
        return self.__fetch_report("byAvailabilityReason", event_key, availability_reason)

    def summary_by_availability_reason(self, event_key):
        return self.__fetch_summary_report("byAvailabilityReason", event_key)

    def deep_summary_by_availability_reason(self, event_key):
        return self.__fetch_deep_summary_report("byAvailabilityReason", event_key)

    def by_channel(self, event_key, channel=None):
        return self.__fetch_report("byChannel", event_key, channel)

    def summary_by_channel(self, event_key):
        return self.__fetch_summary_report("byChannel", event_key)

    def deep_summary_by_channel(self, event_key):
        return self.__fetch_deep_summary_report("byChannel", event_key)

    def __fetch_report(self, report_type, event_key, report_filter=None):
        if report_filter:
            url = "/reports/events/{key}/{reportType}/{filter}"
            body = self.http_client.url(url, key=event_key, reportType=report_type, filter=report_filter).get()
            result = []
            if report_filter not in body:
                return []
            for i in body[report_filter]:
                result.append(EventObjectInfo(i))
            return result
        else:
            url = "/reports/events/{key}/{reportType}"
            body = self.http_client.url(url, key=event_key, reportType=report_type).get()
            return EventReport(body)

    def __fetch_summary_report(self, report_type, event_key):
        url = "/reports/events/{key}/{reportType}/summary"
        return self.http_client.url(url, key=event_key, reportType=report_type).get()

    def __fetch_deep_summary_report(self, report_type, event_key):
        url = "/reports/events/{key}/{reportType}/summary/deep"
        return self.http_client.url(url, key=event_key, reportType=report_type).get()
