from bunch import bunchify

from seatsio.domain import Chart
from seatsio.httpClient import POST, GET, HttpClient


class Client:

    def __init__(self, secret_key, base_url="https://api.seats.io"):
        self.secretKey = secret_key
        self.baseUrl = base_url
        self.httpClient = HttpClient(base_url, secret_key)
        self.charts = Charts(self.httpClient)


class Charts:

    def __init__(self, http_client):
        self.httpClient = http_client

    def retrieve(self, chart_key):
        url = "/charts/" + chart_key
        response = self.httpClient.get(url).execute()
        return bunchify(response.body)

    def create(self, name=None, venue_type=None, categories=None):
        url = "/charts"
        body = {}
        if name:
            body['name'] = name
        if venue_type:
            body['venueType'] = venue_type
        if categories:
            body['categories'] = categories
        response = self.httpClient.post(url).body(body).execute()
        return Chart(response.body)

    def retrieve_published_version(self, key):
        url = "/charts/" + key + "/version/published"
        response = self.httpClient.get(url).execute()
        return bunchify(response.body)

    def add_tag(self, key, tag):
        url = "/charts/" + key + "/tags/" + tag
        response = self.httpClient.post(url).execute()
        return response
