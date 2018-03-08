from bunch import bunchify

from seatsio.domain import Chart
from seatsio.httpClient import POST, GET


class Client:

    def __init__(self, secret_key, base_url = "https://api.seats.io"):
        self.secretKey = secret_key
        self.baseUrl = base_url
        self.charts = Charts(self.secretKey, self.baseUrl)

class Charts:

    def __init__(self, secret_key, base_url):
        self.secretKey = secret_key
        self.baseUrl = base_url

    def retrieve(self, chart_key):
        url = self.baseUrl + "/charts/" + chart_key
        response = GET(url).basicAuth(self.secretKey, '').execute()
        return bunchify(response.body)

    def create(self, name=None, venue_type=None, categories=None):
        url = self.baseUrl + "/charts"
        body = {}
        if name: body['name'] = name
        if venue_type: body['venueType'] = venue_type
        if categories: body['categories'] = categories
        response = POST(url).basicAuth(self.secretKey, '').body(body).execute()
        return Chart(response.body)

    def retrievePublishedVersion(self, key):
        url = self.baseUrl + "/charts/" + key + "/version/published"
        response = GET(url).basicAuth(self.secretKey, '').execute()
        return bunchify(response.body)

    def addTag(self, key, tag):
        url = self.baseUrl + "/charts/" + key + "/tags/" + tag
        response = POST(url).basicAuth(self.secretKey, '').execute()
        return response



