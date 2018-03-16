from bunch import bunchify

from seatsio.domain import Event, StatusChange, ObjectStatus, BestAvailableObjects, ObjectProperties, EventReport, \
    EventReportItem
from seatsio.pagination.lister import Lister
from seatsio.pagination.pageFetcher import PageFetcher


class EventRequest:
    def __init__(self, chart_key, event_key=None, book_whole_tables=None):
        if chart_key:
            self.chartKey = chart_key
        if event_key:
            self.eventKey = event_key
        if book_whole_tables is not None:
            self.bookWholeTables = book_whole_tables


class ChangeObjectStatusRequest:
    def __init__(self, object_or_objects, status, hold_token, order_id, event_key_or_keys):
        self.objects = self.__normalize_objects(object_or_objects)
        self.status = status
        if hold_token:
            self.holdToken = hold_token
        if order_id:
            self.orderId = order_id
        if isinstance(event_key_or_keys, basestring):
            self.events = [event_key_or_keys]
        else:
            self.events = event_key_or_keys

    def __normalize_objects(self, object_or_objects):
        if isinstance(object_or_objects, list):
            if len(object_or_objects) == 0:
                return []
            if isinstance(object_or_objects[0], ObjectProperties):
                return object_or_objects
            if isinstance(object_or_objects[0], basestring):
                result = []
                for o in object_or_objects:
                    result.append(ObjectProperties(o))
                return result
            else:
                raise Exception("Unsupported type " + str(type(object_or_objects[0])))
        return self.__normalize_objects([object_or_objects])


class ChangeBestAvailableObjectStatusRequest:
    def __init__(self, number, categories, extra_data, status, hold_token, order_id):
        best_available = {"number": number}
        if categories:
            best_available["categories"] = categories
        if extra_data:
            best_available["extraData"] = extra_data
        self.bestAvailable = best_available
        self.status = status
        if hold_token:
            self.holdToken = hold_token
        if order_id:
            self.orderId = order_id


class ExtraDataRequest:
    def __init__(self, extra_data):
        if extra_data:
            self.extraData = extra_data


class ForSaleRequest:
    def __init__(self, objects, categories):
        if objects:
            self.objects = objects
        if categories:
            self.categories = categories


class EventsClient:

    def __init__(self, http_client):
        self.http_client = http_client
        self.reports = EventReports(self.http_client)

    def create(self, chart_key):
        response = self.http_client.url("/events").post(EventRequest(chart_key=chart_key))
        return Event(response.body)

    def update(self, key, chart_key=None, event_key=None, book_whole_tables=None):
        self.http_client.url("/events/{key}", key=key).post(EventRequest(chart_key, event_key, book_whole_tables))

    def retrieve(self, key):
        return self.http_client.url("/events/{key}", key=key).get_as(Event)

    def list(self):
        return Lister(PageFetcher(Event, self.http_client, "/events"))

    def status_changes(self, key, object_id=None):
        if object_id:
            return Lister(self.status_changes_for_object(key, object_id))
        else:
            return Lister(PageFetcher(StatusChange, self.http_client, "/events/{key}/status-changes", key=key))

    def status_changes_for_object(self, key, object_id):
        url = "/events/{key}/objects/{objectId}/status-changes"
        return PageFetcher(StatusChange, self.http_client, url, key=key, objectId=object_id)

    def book(self, event_key_or_keys, object_or_objects, hold_token=None, order_id=None):
        self.change_object_status(event_key_or_keys, object_or_objects, ObjectStatus.BOOKED, hold_token, order_id)

    def book_best_available(self, event_key, number, categories=None, hold_token=None, order_id=None):
        return self.change_best_available_object_status(
            event_key,
            number,
            ObjectStatus.BOOKED,
            categories,
            hold_token,
            order_id
        )

    def hold_best_available(self, event_key, number, categories=None, hold_token=None, order_id=None):
        return self.change_best_available_object_status(
            event_key,
            number,
            ObjectStatus.HELD,
            categories,
            hold_token,
            order_id
        )

    def change_best_available_object_status(
            self, event_key, number, status, categories=None, hold_token=None, extra_data=None, order_id=None):
        response = self.http_client.url("/events/{key}/actions/change-object-status", key=event_key).post(
            ChangeBestAvailableObjectStatusRequest(
                number=number,
                status=status,
                categories=categories,
                hold_token=hold_token,
                extra_data=extra_data,
                order_id=order_id
            ))
        return BestAvailableObjects(response.body)

    def release(self, event_key_or_keys, object_or_objects, hold_token=None, order_id=None):
        self.change_object_status(event_key_or_keys, object_or_objects, ObjectStatus.FREE, hold_token, order_id)

    def hold(self, event_key_or_keys, object_or_objects, hold_token, order_id=None):
        self.change_object_status(event_key_or_keys, object_or_objects, ObjectStatus.HELD, hold_token, order_id)

    def change_object_status(self, event_key_or_keys, object_or_objects, status, hold_token=None, order_id=None):
        request = ChangeObjectStatusRequest(object_or_objects, status, hold_token, order_id, event_key_or_keys)
        self.http_client.url("/seasons/actions/change-object-status").post(request)

    def retrieve_object_status(self, key, object_key):
        return self.http_client.url("/events/{key}/objects/{object}", key=key, object=object_key).get_as(ObjectStatus)

    def mark_as_for_sale(self, event_key, objects=None, categories=None):
        self.http_client \
            .url("/events/{key}/actions/mark-as-for-sale", key=event_key) \
            .post(ForSaleRequest(objects, categories))

    def mark_as_not_for_sale(self, key, objects=None, categories=None):
        self.http_client \
            .url("/events/{key}/actions/mark-as-not-for-sale", key=key) \
            .post(ForSaleRequest(objects, categories))

    def mark_everything_as_for_sale(self, key):
        self.http_client.url("/events/{key}/actions/mark-everything-as-for-sale", key=key).post()

    def update_extra_data(self, key, o, extra_data):
        self.http_client \
            .url("/events/{key}/objects/{object}/actions/update-extra-data", key=key, object=o) \
            .post(ExtraDataRequest(extra_data))


class EventReports:
    def __init__(self, http_client):
        self.http_client = http_client

    def by_status(self, event_key, status=None):
        return self.__fetch_report("byStatus", event_key, status)

    def by_category_label(self, event_key, category_label=None):
        return self.__fetch_report("byCategoryLabel", event_key, category_label)

    def by_category_key(self, event_key, category_key=None):
        return self.__fetch_report("byCategoryKey", event_key, category_key)

    def by_label(self, event_key, label=None):
        return self.__fetch_report("byLabel", event_key, label)

    def by_order_id(self, event_key, order_id=None):
        return self.__fetch_report("byOrderId", event_key, order_id)

    def by_section(self, event_key, section=None):
        return self.__fetch_report("bySection", event_key, section)

    def __fetch_report(self, report_type, event_key, report_filter=None):
        if report_filter:
            url = "/reports/events/{key}/{reportType}/{filter}"
            body = self.http_client.url(url, key=event_key, reportType=report_type, filter=report_filter).get().body
            result = []
            for i in body[report_filter]:
                result.append(EventReportItem(i))
            return result
        else:
            url = "/reports/events/{key}/{reportType}"
            body = self.http_client.url(url, key=event_key, reportType=report_type).get().body
            return EventReport(body)
