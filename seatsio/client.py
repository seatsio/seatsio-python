import urllib

from bunch import bunchify

from seatsio.domain import Chart, Event
from seatsio.httpClient import HttpClient


class Client:

    def __init__(self, secret_key, base_url="https://api.seats.io"):
        self.baseUrl = base_url
        self.httpClient = HttpClient(base_url, secret_key)
        self.charts = Charts(self.httpClient)
        self.events = Events(self.httpClient)


class Charts():

    def __init__(self, http_client):
        self.httpClient = http_client

    def retrieve(self, chart_key):
        url = "/charts/{key}".format(key=chart_key)
        response = self.httpClient.get(url)
        return Chart(response.body)

    def retrieve_with_events(self, chart_key):
        url = "/charts/{key}?expand=events".format(key=chart_key)
        response = self.httpClient.get(url)
        return Chart(response.body)

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
        url = "/charts/{key}/version/published".format(key=key)
        response = self.httpClient.get(url)
        return bunchify(response.body)

    def copy(self, key):
        url = "/charts/{key}/version/published/actions/copy".format(key=key)
        response = self.httpClient.post(url)
        return Chart(response.body)

    def copy_draft_version(self, key):
        url = "/charts/{key}/version/draft/actions/copy".format(key=key)
        response = self.httpClient.post(url)
        return Chart(response.body)

    def update(self, key, name):
        url = "/charts/{key}".format(key=key)
        body = {}
        if (name):
            body['name'] = name
        self.httpClient.post(url, body)

    def add_tag(self, key, tag):
        url = "/charts/{key}/tags/{tag}".format(key=key, tag=urllib.quote(tag, safe=''))
        return self.httpClient.post(url)


class Events:

    def __init__(self, http_client):
        self.httpClient = http_client

    def create(self, chart_key):
        url = "/events"
        body = {"chartKey": chart_key}
        response = self.httpClient.post(url, body)
        return Event(response.body)
