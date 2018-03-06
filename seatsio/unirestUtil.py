from urllib2 import URLError

import unirest

from seatsio.exceptions import SeatsioException


class Get:
    def __init__(self, url):
        self.httpMethod = "GET"
        self.url = url

    def basicAuth(self, username, password):
        self.auth = (username, password)
        return self

    def execute(self):
        try:
            response = unirest.get(self.url, auth=self.auth)
            if response.code >= 400:
                raise SeatsioException(self, response)
            else:
                return response
        except URLError:
            raise SeatsioException(self)
