from bunch import bunchify

from seatsio.domain import Chart, Event, Subaccount, HoldToken
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
        return Lister(PageFetcher(self.http_client, "/charts", Chart))

    def archive(self):
        return Lister(PageFetcher(self.http_client, "/charts/archive", Chart))


class Events:

    def __init__(self, http_client):
        self.httpClient = http_client

    def create(self, chart_key):
        body = {"chartKey": chart_key}
        response = self.httpClient.url("/events").post(body)
        return Event(response.body)


class Subaccounts:
    def __init__(self, http_client):
        self.http_client = http_client

    def create(self, name=None):
        body = {}
        if (name):
            body['name'] = name
        response = self.http_client.url("/subaccounts").post(body)
        return Subaccount(response.body)

    def update(self, id, new_name):
        body = {}
        if (new_name):
            body['name'] = new_name
        self.http_client.url("/subaccounts/{id}", id=id).post(body)

    def retrieve(self, subaccount_id):
        response = self.http_client.url("/subaccounts/{id}", id=subaccount_id).get()
        return Subaccount(response.body)

    def activate(self, subaccount_id):
        self.http_client.url("/subaccounts/{id}/actions/activate", id=subaccount_id).post()

    def deactivate(self, subaccount_id):
        self.http_client.url("/subaccounts/{id}/actions/deactivate", id=subaccount_id).post()

    def copy_chart_to_parent(self, id, chart_key):
        response = self.http_client.url(
            "/subaccounts/{id}/charts/{chartKey}/actions/copy-to/parent",
            id=id,
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
        return Lister(PageFetcher(self.http_client, "/subaccounts", Subaccount))

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
