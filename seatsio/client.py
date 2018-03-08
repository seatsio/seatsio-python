from bunch import bunchify

from seatsio.domain import Chart, Event
from seatsio.httpClient import HttpClient


class Client:

    def __init__(self, secret_key, base_url="https://api.seats.io"):
        self.baseUrl = base_url
        self.httpClient = HttpClient(base_url, secret_key)
        self.charts = Charts(self.httpClient, Chart)
        self.events = Events(self.httpClient, Event)


class ApiResource:

    def __init__(self, http_client, cls):
        self.httpClient = http_client
        self.cls = cls

    def get(self, relative_url, *params):
        response = self.httpClient.get(relative_url)
        return self.cls(response.body)


class Charts(ApiResource):

    def retrieve(self, chart_key):
        url = "/charts/" + chart_key
        return self.get(url)

    def retrieve_with_events(self, chart_key):
        url = "/charts/" + chart_key + "?expand=events"
        return self.get(url)

    def create(self, name=None, venue_type=None, categories=None):
        url = "/charts"
        body = {}
        if name:
            body['name'] = name
        if venue_type:
            body['venueType'] = venue_type
        if categories:
            body['categories'] = categories
        response = self.httpClient.post(url, body)
        return Chart(response.body)

    def retrieve_published_version(self, key):
        url = "/charts/" + key + "/version/published"
        response = self.httpClient.get(url)
        return bunchify(response.body)

    def copy(self, key):
        url = "/charts/" + key + "/version/published/actions/copy"
        response = self.httpClient.post(url)
        return Chart(response.body)

    def copy_draft_version(self, key):
        url = "/charts/" + key + "/version/draft/actions/copy"
        response = self.httpClient.post(url)
        return Chart(response.body)

    def update(self, key, name):
        url = "/charts/" + key
        body = {}
        if (name):
            body['name'] = name
        self.httpClient.post(url, body)

    def add_tag(self, key, tag):
        url = "/charts/" + key + "/tags/" + tag
        return self.httpClient.post(url)


class Events(ApiResource):

    def create(self, chart_key):
        url = "/events"
        body = {"chartKey": chart_key}
        response = self.httpClient.post(url, body)
        return Event(response.body)
