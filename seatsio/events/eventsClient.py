from seatsio.domain import Event, StatusChange, BestAvailableObjects, ChangeObjectStatusResult, EventObjectInfo, \
    event_from_json
from seatsio.events.changeBestAvailableObjectStatusRequest import ChangeBestAvailableObjectStatusRequest
from seatsio.events.changeObjectStatusRequest import ChangeObjectStatusRequest
from seatsio.events.channelsClient import ChannelsClient
from seatsio.events.createMultipleEventsRequest import CreateMultipleEventsRequest
from seatsio.events.createSingleEventRequest import CreateSingleEventRequest
from seatsio.events.extraDataRequest import ExtraDataRequest
from seatsio.events.forSaleRequest import ForSaleRequest
from seatsio.events.overrideSeasonObjectStatusRequest import OverrideSeasonObjectStatusRequest
from seatsio.events.updateEventRequest import UpdateEventRequest
from seatsio.pagination.listableObjectsClient import ListableObjectsClient
from seatsio.pagination.lister import Lister
from seatsio.pagination.pageFetcher import PageFetcher
from seatsio.reports.events.eventReports import EventReports


class EventsClient(ListableObjectsClient):

    def __init__(self, http_client):
        ListableObjectsClient.__init__(self, http_client, event_from_json, "/events")
        self.reports = EventReports(self.http_client)
        self.channels = ChannelsClient(self.http_client)

    def create(self, chart_key, event_key=None, name=None, date=None, table_booking_config=None,
               object_categories=None, categories=None, channels=None, for_sale_config=None):
        response = self.http_client.url("/events").post(
            CreateSingleEventRequest(chart_key, event_key, name, date, table_booking_config,
                                     object_categories, categories, channels, for_sale_config))
        return Event(response.json())

    def create_multiple(self, chart_key, events_properties):
        response = self.http_client.url("/events/actions/create-multiple").post(
            CreateMultipleEventsRequest(chart_key, events_properties))
        return Event.create_list(response.json().get("events"))

    def update(self, key, event_key=None, name=None, date=None, table_booking_config=None,
               object_categories=None, categories=None, is_in_the_past=None):
        request = UpdateEventRequest(event_key, name, date, table_booking_config, object_categories, categories,
                                     is_in_the_past)
        self.http_client.url("/events/{key}", key=key).post(
            request)

    def remove_object_categories(self, key):
        self.update(key, object_categories={})

    def remove_categories(self, key):
        self.update(key, categories=[])

    def delete(self, key):
        self.http_client.url("/events/{key}", key=key).delete()

    def retrieve(self, key):
        return self.http_client.url("/events/{key}", key=key).get_as(event_from_json)

    def status_changes(self, key, filter=None, sort_field=None, sort_direction=None):
        page_fetcher = PageFetcher(StatusChange, self.http_client, "/events/{key}/status-changes", key=key)
        page_fetcher.set_query_param("filter", filter)
        page_fetcher.set_query_param("sort", self.to_sort(sort_field, sort_direction))
        return Lister(page_fetcher)

    @staticmethod
    def to_sort(sort_field, sort_direction):
        if sort_field is None:
            return None
        elif sort_direction is None:
            return sort_field
        else:
            return sort_field + ":" + sort_direction

    def status_changes_for_object(self, key, object_id):
        url = "/events/{key}/objects/{objectId}/status-changes"
        page_fetcher = PageFetcher(StatusChange, self.http_client, url, key=key, objectId=object_id)
        return Lister(page_fetcher)

    def book(self, event_key_or_keys, object_or_objects, hold_token=None, order_id=None, keep_extra_data=None,
             ignore_channels=None, channel_keys=None):
        return self.change_object_status(event_key_or_keys, object_or_objects, EventObjectInfo.BOOKED, hold_token,
                                         order_id, keep_extra_data, ignore_channels, channel_keys)

    def put_up_for_resale(self, event_key_or_keys, object_or_objects, resale_listing_id=None):
        return self.change_object_status(event_key_or_keys, object_or_objects, EventObjectInfo.RESALE, None, None, None, None, None, None, None, resale_listing_id)

    def book_best_available(self, event_key, number, categories=None, hold_token=None, extra_data=None,
                            ticket_types=None, order_id=None, keep_extra_data=None, ignore_channels=None,
                            channel_keys=None, try_to_prevent_orphan_seats=None, zone=None):
        return self.change_best_available_object_status(
            event_key,
            number,
            EventObjectInfo.BOOKED,
            categories,
            hold_token,
            extra_data,
            ticket_types,
            order_id,
            keep_extra_data,
            ignore_channels,
            channel_keys,
            try_to_prevent_orphan_seats,
            zone
        )

    def hold_best_available(self, event_key, number, categories=None, hold_token=None, extra_data=None,
                            ticket_types=None, order_id=None, keep_extra_data=None, ignore_channels=None,
                            channel_keys=None, try_to_prevent_orphan_seats=None, zone=None):
        return self.change_best_available_object_status(
            event_key,
            number,
            EventObjectInfo.HELD,
            categories,
            hold_token,
            extra_data,
            ticket_types,
            order_id,
            keep_extra_data,
            ignore_channels,
            channel_keys,
            try_to_prevent_orphan_seats,
            zone
        )

    def change_best_available_object_status(self, event_key, number, status, categories=None, hold_token=None,
                                            extra_data=None, ticket_types=None, order_id=None, keep_extra_data=None,
                                            ignore_channels=None, channel_keys=None, try_to_prevent_orphan_seats=None,
                                            zone=None, sections=None, accessible_seats=None):
        response = self.http_client.url("/events/{key}/actions/change-object-status", key=event_key).post(
            ChangeBestAvailableObjectStatusRequest(number, categories, zone, sections, extra_data, ticket_types, status,
                                                   hold_token, order_id, keep_extra_data, ignore_channels, channel_keys,
                                                   try_to_prevent_orphan_seats, accessible_seats))
        return BestAvailableObjects(response.json())

    def release(self, event_key_or_keys, object_or_objects, hold_token=None, order_id=None, keep_extra_data=None,
                ignore_channels=None, channel_keys=None):
        request = ChangeObjectStatusRequest(
            'RELEASE', object_or_objects, None, hold_token, order_id, event_key_or_keys,
            keep_extra_data, ignore_channels, channel_keys)
        return self.__do_change_status(request)

    def hold(self, event_key_or_keys, object_or_objects, hold_token, order_id=None, keep_extra_data=None,
             ignore_channels=None, channel_keys=None):
        return self.change_object_status(event_key_or_keys, object_or_objects, EventObjectInfo.HELD, hold_token,
                                         order_id, keep_extra_data, ignore_channels, channel_keys)

    def change_object_status(self, event_key_or_keys, object_or_objects, status, hold_token=None, order_id=None,
                             keep_extra_data=None, ignore_channels=None, channel_keys=None,
                             allowed_previous_statuses=None, rejected_previous_statuses=None, resale_listing_id=None):
        request = ChangeObjectStatusRequest('CHANGE_STATUS_TO', object_or_objects, status, hold_token, order_id, event_key_or_keys,
                                            keep_extra_data, ignore_channels, channel_keys,
                                            allowed_previous_statuses, rejected_previous_statuses, resale_listing_id)
        return self.__do_change_status(request)

    def __do_change_status(self, request):
        response = self.http_client.url("/events/groups/actions/change-object-status",
                                        query_params={"expand": "objects"}).post(request)
        return ChangeObjectStatusResult(response.json())

    def change_object_status_in_batch(self, status_change_requests):
        requests = list(
            map(lambda r: self.__change_object_status_in_batch_request(r.type, r.event_key, r.object_or_objects, r.status,
                                                                       r.hold_token, r.order_id, r.keep_extra_data,
                                                                       r.ignore_channels, r.channel_keys,
                                                                       r.allowed_previous_statuses, r.rejected_previous_statuses, r.resale_listing_id),
                status_change_requests))
        response = self.http_client.url("/events/actions/change-object-status",
                                        query_params={"expand": "objects"}).post({"statusChanges": requests})
        return list(map(lambda r: ChangeObjectStatusResult(r), response.json().get("results")))

    def __change_object_status_in_batch_request(self, type, event_key, object_or_objects, status, hold_token, order_id,
                                                keep_extra_data, ignore_channels, channel_keys,
                                                allowed_previous_statuses, rejected_previous_statuses, resale_listing_id):
        request = ChangeObjectStatusRequest(type, object_or_objects, status, hold_token, order_id, "", keep_extra_data,
                                            ignore_channels, channel_keys, allowed_previous_statuses,
                                            rejected_previous_statuses, resale_listing_id)
        request.event = event_key
        delattr(request, "events")
        return request

    def retrieve_object_info(self, key, object_label):
        result = self.retrieve_object_infos(key, [object_label])
        return result[object_label]

    def retrieve_object_infos(self, key, object_labels):
        query_params = {"label": object_labels}
        response_body = self.http_client.url("/events/{key}/objects", query_params, key=key).get()
        items = {}
        for key, value in response_body.items():
            items[key] = EventObjectInfo(value)
        return items

    def mark_as_for_sale(self, event_key, objects=None, area_places=None, categories=None):
        self.http_client \
            .url("/events/{key}/actions/mark-as-for-sale", key=event_key) \
            .post(ForSaleRequest(objects, area_places, categories))

    def mark_as_not_for_sale(self, key, objects=None, area_places=None, categories=None):
        self.http_client \
            .url("/events/{key}/actions/mark-as-not-for-sale", key=key) \
            .post(ForSaleRequest(objects, area_places, categories))

    def mark_everything_as_for_sale(self, key):
        self.http_client.url("/events/{key}/actions/mark-everything-as-for-sale", key=key).post()

    def override_season_object_status(self, key, objects):
        self.http_client \
            .url("/events/{key}/actions/override-season-status", key=key) \
            .post(OverrideSeasonObjectStatusRequest(objects))

    def use_season_object_status(self, key, objects):
        self.http_client \
            .url("/events/{key}/actions/use-season-status", key=key) \
            .post(OverrideSeasonObjectStatusRequest(objects))

    def update_extra_data(self, key, o, extra_data):
        self.http_client \
            .url("/events/{key}/objects/{object}/actions/update-extra-data", key=key, object=o) \
            .post(ExtraDataRequest(extra_data))

    def update_extra_datas(self, key, extra_datas):
        self.http_client \
            .url("/events/{key}/actions/update-extra-data", key=key) \
            .post(ExtraDataRequest(extra_datas))
