import jsonpickle
import unirest
from bunch import bunchify

from seatsio.domain import Chart
from seatsio.exceptions import SeatsioException


class SeatsioClient:

    def __init__(self, secret_key, base_url):
        self.secretKey = secret_key
        self.baseUrl = base_url

    def charts(self):
        return Charts(self.secretKey, self.baseUrl)


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





class GET:
    def __init__(self, url):
        self.httpMethod = "GET"
        self.url = url

    def basicAuth(self, username, password):
        self.auth = (username, password)
        return self

    def execute(self):
        response = self.__try_execute()
        if response.code >= 400:
            raise SeatsioException(self, response)
        else:
            return response

    def __try_execute(self):
        try:
            return unirest.get(self.url, auth=self.auth)
        except Exception as cause:
            raise SeatsioException(self, cause=cause)


class POST:
    def __init__(self, url):
        self.httpMethod = "POST"
        self.url = url
        self.bodyObject = None

    def basicAuth(self, username, password):
        self.auth = (username, password)
        return self

    def body(self, body):
        self.bodyObject = body
        return self

    def execute(self):
        response = self.__try_execute()
        if response.code >= 400:
            raise SeatsioException(self, response)
        else:
            return response

    def __try_execute(self):
        try:
            if self.bodyObject:
                json = jsonpickle.encode(self.bodyObject, unpicklable=False)
                return unirest.post(
                    url=self.url,
                    auth=self.auth,
                    headers={"Accept": "application/json"},
                    params=json
                )
            else:
                return unirest.post(
                    url=self.url,
                    auth=self.auth
                )
        except Exception as cause:
            raise SeatsioException(self, cause=cause)
