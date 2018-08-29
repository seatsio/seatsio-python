from seatsio.domain import Event, StatusChange, ObjectStatus, BestAvailableObjects, ChangeObjectStatusResult
from seatsio.events.changeBestAvailableObjectStatusRequest import ChangeBestAvailableObjectStatusRequest
from seatsio.events.changeObjectStatusRequest import ChangeObjectStatusRequest
from seatsio.events.eventReports import EventReports
from seatsio.events.eventRequest import EventRequest
from seatsio.events.extraDataRequest import ExtraDataRequest
from seatsio.events.forSaleRequest import ForSaleRequest
from seatsio.pagination.listableObjectsClient import ListableObjectsClient
from seatsio.pagination.lister import Lister
from seatsio.pagination.pageFetcher import PageFetcher


class EventsClient(ListableObjectsClient):

    def __init__(self, http_client):
        ListableObjectsClient.__init__(self, http_client, Event, "/events")
        self.reports = EventReports(self.http_client)

    def create(self, chart_key, event_key=None, book_whole_tables=None):
        response = self.http_client.url("/events").post(EventRequest(chart_key, event_key, book_whole_tables))
        return Event(response.json())

    def update(self, key, chart_key=None, event_key=None, book_whole_tables=None):
        self.http_client.url("/events/{key}", key=key).post(EventRequest(chart_key, event_key, book_whole_tables))

    def delete(self, key):
        self.http_client.url("/events/{key}", key=key).delete()

    def retrieve(self, key):
        return self.http_client.url("/events/{key}", key=key).get_as(Event)

    def list_status_changes(self, key, object_id=None):
        if object_id is not None:
            return Lister(self.status_changes_for_object(key, object_id)).list()
        else:
            return Lister(PageFetcher(StatusChange, self.http_client, "/events/{key}/status-changes", key=key)).list()

    def status_changes_for_object(self, key, object_id):
        url = "/events/{key}/objects/{objectId}/status-changes"
        return PageFetcher(StatusChange, self.http_client, url, key=key, objectId=object_id)

    def book(self, event_key_or_keys, object_or_objects, hold_token=None, order_id=None):
        return self.change_object_status(event_key_or_keys, object_or_objects, ObjectStatus.BOOKED, hold_token, order_id)

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
        return BestAvailableObjects(response.json())

    def release(self, event_key_or_keys, object_or_objects, hold_token=None, order_id=None):
        return self.change_object_status(event_key_or_keys, object_or_objects, ObjectStatus.FREE, hold_token, order_id)

    def hold(self, event_key_or_keys, object_or_objects, hold_token, order_id=None):
        return self.change_object_status(event_key_or_keys, object_or_objects, ObjectStatus.HELD, hold_token, order_id)

    def change_object_status(self, event_key_or_keys, object_or_objects, status, hold_token=None, order_id=None):
        request = ChangeObjectStatusRequest(object_or_objects, status, hold_token, order_id, event_key_or_keys)
        response = self.http_client.url("/seasons/actions/change-object-status", query_params={"expand": "labels"}).post(request)
        return ChangeObjectStatusResult(response.json())

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

    def update_extra_datas(self, key, extra_datas):
        self.http_client \
            .url("/events/{key}/actions/update-extra-data", key=key) \
            .post(ExtraDataRequest(extra_datas))
