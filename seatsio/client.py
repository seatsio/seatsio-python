from seatsio.charts.chartsClient import ChartsClient
from seatsio.domain import *
from seatsio.events.eventsClient import EventsClient
from seatsio.httpClient import HttpClient
from seatsio.pagination.lister import Lister
from seatsio.pagination.pageFetcher import PageFetcher


class Client:
    def __init__(self, secret_key, base_url="https://api.seats.io"):
        self.base_url = base_url
        self.http_client = HttpClient(base_url, secret_key)
        self.charts = ChartsClient(self.http_client)
        self.events = EventsClient(self.http_client)
        self.subaccounts = Subaccounts(self.http_client)
        self.hold_tokens = HoldTokens(self.http_client)


class Subaccounts:

    def __init__(self, http_client):
        self.http_client = http_client

    def create(self, name=None):
        body = {}
        if name:
            body['name'] = name
        response = self.http_client.url("/subaccounts").post(body)
        return Subaccount(response.json())

    def update(self, subaccount_id, new_name):
        body = {}
        if new_name:
            body['name'] = new_name
        self.http_client.url("/subaccounts/{id}", id=subaccount_id).post(body)

    def retrieve(self, subaccount_id):
        response = self.http_client.url("/subaccounts/{id}", id=subaccount_id).get()
        return Subaccount(response)

    def activate(self, subaccount_id):
        self.http_client.url("/subaccounts/{id}/actions/activate", id=subaccount_id).post()

    def deactivate(self, subaccount_id):
        self.http_client.url("/subaccounts/{id}/actions/deactivate", id=subaccount_id).post()

    def copy_chart_to_parent(self, subaccount_id, chart_key):
        response = self.http_client.url(
            "/subaccounts/{id}/charts/{chartKey}/actions/copy-to/parent",
            id=subaccount_id,
            chartKey=chart_key).post()
        return Chart(response.json())

    def copy_chart_to_subaccount(self, from_id, to_id, chart_key):
        response = self.http_client.url(
            "/subaccounts/{fromId}/charts/{chartKey}/actions/copy-to/{toId}",
            fromId=from_id,
            toId=to_id,
            chartKey=chart_key).post()
        # TODO refactor all Chart(response.json()) calls
        return Chart(response.json())

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
        return HoldToken(response.json())

    def retrieve(self, hold_token):
        response = self.http_client.url("/hold-tokens/{holdToken}", holdToken=hold_token).get()
        return HoldToken(response)

    def expire_in_minutes(self, hold_token, expires_in_minutes):
        body = {}
        if expires_in_minutes:
            body["expiresInMinutes"] = expires_in_minutes
        response = self.http_client.url("/hold-tokens/{holdToken}", holdToken=hold_token).post(body)
        return HoldToken(response.json())
