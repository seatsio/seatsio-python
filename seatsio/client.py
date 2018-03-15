from seatsio.domain import *
from seatsio.httpClient import HttpClient
from seatsio.pagination.lister import Lister
from seatsio.pagination.pageFetcher import PageFetcher


class Client:

    def __init__(self, secret_key, base_url="https://api.seats.io"):
        self.baseUrl = base_url
        self.httpClient = HttpClient(base_url, secret_key)
        self.charts = Charts(self.httpClient)
        self.events = Events(self.httpClient)
        self.subaccounts = Subaccounts(self.httpClient)
        self.hold_tokens = HoldTokens(self.httpClient)


class Charts:

    def __init__(self, http_client):
        self.http_client = http_client

    def retrieve(self, chart_key):
        response = self.http_client.url("/charts/{key}", key=chart_key).get()
        return Chart(response.body)

    def retrieve_with_events(self, chart_key):
        response = self.http_client.url("/charts/{key}?expand=events", key=chart_key).get()
        return Chart(response.body)

    def create(self, name=None, venue_type=None, categories=None):
        body = {}
        if name:
            body['name'] = name
        if venue_type:
            body['venueType'] = venue_type
        if categories:
            body['categories'] = categories
        response = self.http_client.url("/charts").post(body)
        return Chart(response.body)

    def retrieve_published_version(self, key):
        response = self.http_client.url("/charts/{key}/version/published", key=key).get()
        return bunchify(response.body)

    def retrieve_draft_version(self, key):
        response = self.http_client.url("/charts/{key}/version/draft", key=key).get()
        return bunchify(response.body)

    def retrieve_draft_version_thumbnail(self, key):
        response = self.http_client.url("/charts/{key}/version/draft/thumbnail", key=key).get()
        return response.raw_body

    def retrieve_published_version_thumbnail(self, key):
        response = self.http_client.url("/charts/{key}/version/published/thumbnail", key=key).get()
        return response.raw_body

    def copy(self, key):
        response = self.http_client.url("/charts/{key}/version/published/actions/copy", key=key).post()
        return Chart(response.body)

    def copy_to_subaccount(self, chart_key, subaccount_id):
        response = self.http_client.url("/charts/{key}/version/published/actions/copy-to/{subaccountId}",
                                        key=chart_key,
                                        subaccountId=subaccount_id).post()
        return Chart(response.body)

    def copy_draft_version(self, key):
        response = self.http_client.url("/charts/{key}/version/draft/actions/copy", key=key).post()
        return Chart(response.body)

    def discard_draft_version(self, key):
        self.http_client.url("/charts/{key}/version/draft/actions/discard", key=key).post()

    def update(self, key, new_name=None, categories=None):
        body = {}
        if new_name:
            body['name'] = new_name
        if categories:
            body['categories'] = categories
        self.http_client.url("/charts/{key}", key=key).post(body)

    def move_to_archive(self, chart_key):
        self.http_client.url("/charts/{key}/actions/move-to-archive", key=chart_key).post()

    def move_out_of_archive(self, chart_key):
        self.http_client.url("/charts/{key}/actions/move-out-of-archive", key=chart_key).post()

    def publish_draft_version(self, chart_key):
        self.http_client.url("/charts/{key}/version/draft/actions/publish", key=chart_key).post()

    def list_all_tags(self):
        response = self.http_client.url("/charts/tags").get()
        return response.body["tags"]

    def add_tag(self, key, tag):
        return self.http_client.url("/charts/{key}/tags/{tag}", key=key, tag=tag).post()

    def remove_tag(self, key, tag):
        self.http_client.url("/charts/{key}/tags/{tag}", key=key, tag=tag).delete()

    def list(self):
        return Lister(PageFetcher(Chart, self.http_client, "/charts"))

    def archive(self):
        return Lister(PageFetcher(Chart, self.http_client, "/charts/archive"))


class Events:

    def __init__(self, http_client):
        self.httpClient = http_client
        self.reports = EventReports(self.httpClient)

    def create(self, chart_key):
        body = {"chartKey": chart_key}
        response = self.httpClient.url("/events").post(body)
        return Event(response.body)

    def update(self, key, chart_key=None, event_key=None, book_whole_tables=None):
        body = {}
        if (chart_key):
            body["chartKey"] = chart_key
        if event_key:
            body["eventKey"] = event_key
        if book_whole_tables is not None:
            body["bookWholeTables"] = book_whole_tables
        self.httpClient.url("/events/{key}", key=key).post(body)

    def retrieve(self, key):
        response = self.httpClient.url("/events/{key}", key=key).get()
        return Event(response.body)

    def list(self):
        return Lister(PageFetcher(Event, self.httpClient, "/events"))

    def status_changes(self, key, object_id=None):
        if object_id:
            return Lister(
                PageFetcher(StatusChange, self.httpClient, "/events/{key}/objects/{objectId}/status-changes",
                            key=key,
                            objectId=object_id))
        else:
            return Lister(PageFetcher(StatusChange, self.httpClient, "/events/{key}/status-changes", key=key))

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

    def change_best_available_object_status(self, event_key, number, status, categories=None, hold_token=None,
                                            extra_data=None, order_id=None):
        request = {}
        best_available = {}
        best_available["number"] = number
        if categories:
            best_available["categories"] = categories
        if extra_data:
            best_available["extraData"] = extra_data
        request["bestAvailable"] = best_available
        request["status"] = status
        if hold_token:
            request["holdToken"] = hold_token
        if order_id:
            request["orderId"] = order_id
        response = self.httpClient.url("/events/{key}/actions/change-object-status", key=event_key).post(request)
        return BestAvailableObjects(response.body)

    def release(self, event_key_or_keys, object_or_objects, hold_token=None, order_id=None):
        self.change_object_status(event_key_or_keys, object_or_objects, ObjectStatus.FREE, hold_token, order_id)

    def hold(self, event_key_or_keys, object_or_objects, hold_token, order_id=None):
        self.change_object_status(event_key_or_keys, object_or_objects, ObjectStatus.HELD, hold_token, order_id)

    def change_object_status(self, event_key_or_keys, object_or_objects, status, hold_token=None, order_id=None):
        request = {'objects': self.__normalize_objects(object_or_objects), 'status': status}
        if hold_token:
            request['holdToken'] = hold_token
        if order_id:
            request['orderId'] = order_id
        if isinstance(event_key_or_keys, basestring):
            request['events'] = [event_key_or_keys]
        else:
            request["events"] = event_key_or_keys
        self.httpClient.url("/seasons/actions/change-object-status").post(request)

    def retrieve_object_status(self, key, object_key):
        response = self.httpClient.url("/events/{key}/objects/{object}", key=key, object=object_key).get()
        return ObjectStatus(response.body)

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

    def mark_as_for_sale(self, event_key, objects=None, categories=None):
        body = self.__for_sale_request(objects, categories)
        self.httpClient.url("/events/{key}/actions/mark-as-for-sale", key=event_key).post(body)

    def mark_as_not_for_sale(self, key, objects=None, categories=None):
        body = self.__for_sale_request(objects, categories)
        self.httpClient.url("/events/{key}/actions/mark-as-not-for-sale", key=key).post(body)

    def mark_everything_as_for_sale(self, key):
        self.httpClient.url("/events/{key}/actions/mark-everything-as-for-sale", key=key).post()

    def __for_sale_request(self, objects, categories):
        result = {}
        if objects:
            result["objects"] = objects
        if categories:
            result["categories"] = categories
        return result

    def update_extra_data(self, key, o, extra_data):
        body = {}
        if extra_data:
            body["extraData"] = extra_data
        self.httpClient.url("/events/{key}/objects/{object}/actions/update-extra-data", key=key, object=o) \
            .post(body)


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
        result = self.__fetch_raw_report(report_type, event_key, report_filter)
        return self.__map_multi_value_report(result, report_filter)

    def __fetch_raw_report(self, report_type, event_key, filter):
        if (filter):
            url = "/reports/events/{key}/{reportType}/{filter}"
            return self.http_client.url(url, key=event_key, reportType=report_type, filter=filter).get().body
        else:
            url = "/reports/events/{key}/{reportType}"
            return self.http_client.url(url, key=event_key, reportType=report_type).get().body

    def __map_multi_value_report(self, body, report_filter):
        if report_filter:
            return bunchify(body[report_filter])
        else:
            return bunchify(body)


class Subaccounts:
    def __init__(self, http_client):
        self.http_client = http_client

    def create(self, name=None):
        body = {}
        if name:
            body['name'] = name
        response = self.http_client.url("/subaccounts").post(body)
        return Subaccount(response.body)

    def update(self, subaccount_id, new_name):
        body = {}
        if new_name:
            body['name'] = new_name
        self.http_client.url("/subaccounts/{id}", id=subaccount_id).post(body)

    def retrieve(self, subaccount_id):
        response = self.http_client.url("/subaccounts/{id}", id=subaccount_id).get()
        return Subaccount(response.body)

    def activate(self, subaccount_id):
        self.http_client.url("/subaccounts/{id}/actions/activate", id=subaccount_id).post()

    def deactivate(self, subaccount_id):
        self.http_client.url("/subaccounts/{id}/actions/deactivate", id=subaccount_id).post()

    def copy_chart_to_parent(self, subaccount_id, chart_key):
        response = self.http_client.url(
            "/subaccounts/{id}/charts/{chartKey}/actions/copy-to/parent",
            id=subaccount_id,
            chartKey=chart_key).post()
        return Chart(response.body)

    def copy_chart_to_subaccount(self, from_id, to_id, chart_key):
        response = self.http_client.url(
            "/subaccounts/{fromId}/charts/{chartKey}/actions/copy-to/{toId}",
            fromId=from_id,
            toId=to_id,
            chartKey=chart_key).post()
        return Chart(response.body)

    def list(self):
        return Lister(PageFetcher(Subaccount, self.http_client, "/subaccounts"))

    def regenerate_designer_key(self, subaccount_id):
        self.http_client.url("/subaccounts/{id}/designer-key/actions/regenerate", id=subaccount_id).post()

    def regenerate_secret_key(self, subaccount_id):
        self.http_client.url("/subaccounts/{id}/secret-key/actions/regenerate", id=subaccount_id).post()


class HoldTokens:
    def __init__(self, http_client):
        self.http_client = http_client

    def create(self):
        response = self.http_client.url("/hold-tokens").post()
        return HoldToken(response.body)

    def retrieve(self, hold_token):
        response = self.http_client.url("/hold-tokens/{holdToken}", holdToken=hold_token).get()
        return HoldToken(response.body)

    def expire_in_minutes(self, hold_token, expires_in_minutes):
        body = {}
        if expires_in_minutes:
            body["expiresInMinutes"] = expires_in_minutes
        response = self.http_client.url("/hold-tokens/{holdToken}", holdToken=hold_token).post(body)
        return HoldToken(response.body)
